from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Request, HTTPException,responses,Form,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles

from fastapi import APIRouter
from flask import render_template

from datetime import datetime

#from routers.database import collection_shipment_data
from routers.login import get_current_user_from_cookie,User
from models.models import Shipment

from config.config import SETTING
from dotenv import load_dotenv

load_dotenv()

collection_shipment_data = SETTING.SHIPMENT_COLLECTION


router = APIRouter()
templates = Jinja2Templates(directory="html")

#To add css to html
router.mount("/static", StaticFiles(directory="static"), name="static")




#---------------------------------------To store shipment details  --- New shipment-------------------------------------------#

@router.post("/shipment")
def shipment(request: Request,shipment_number :int=Form(...),container_number:int=Form(...), route_details : str=Form(...),goods_type : str = Form(...),device_name :str=Form(...), delivery_date: str=Form(...),po_number :int =Form(...),delivery_number :int=Form(...),NDC_number :int = Form(...),Batch_id : int=Form(...),serial_number : int=Form(...),shipmentdesc :str=Form(...),
             current_user: User = Depends(get_current_user_from_cookie )):
    
    # Parse the input date string
    input_date = datetime.strptime(delivery_date, "%Y-%m-%d")
    
    delivery_date = input_date.strftime("%d-%m-%Y")
    #Right side fields are bought from the form.. and left side fields are defined datatype in models.py
    shipment_data=Shipment(
        email=current_user["email"],
        shipment_number=shipment_number,
        container_number=container_number,
        route_details=route_details,
        goods_type=goods_type,
        device_name=device_name,
        delivery_date=delivery_date,
        po_number=po_number,
        delivery_no=delivery_number,
        NDC_number=NDC_number,
        Batch_id=Batch_id,
        serial_number=serial_number,
        shipment_desc=shipmentdesc
    )
    try:

        shipment_data=dict(shipment_data)
        #To check either shipment number is already exists or not.
        result=collection_shipment_data.find_one({"shipment_number": shipment_number})
        if result:
            return templates.TemplateResponse("shipment.html", {"request": request, "message": "Shipment number already exists."})
        else:
            collection_shipment_data.insert_one(shipment_data)
            return templates.TemplateResponse("shipment.html", {"request": request, "message": "Shipment created successfully."})
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#---------------------------------------------------------get_new_shipment_page--------------------------------------#

@router.get("/shipment")
async def shipment(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    try:
        #if user is none then it is redirected to login page
        if current_user is None:
            return RedirectResponse(url="/login")
        else:
            return templates.TemplateResponse("shipment.html", {"request": request, "user": current_user})
    
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    

#--------------------------------------To get shipment details and display at my shipment page--------------#

@router.get("/myshipment")
def get_myshipment(request: Request, current_user: User = Depends(get_current_user_from_cookie )):
    try:
        if (current_user['Role']).lower()=="admin" or (current_user['Role']).lower()=="super admin":
            shipment_data=list(collection_shipment_data.find({}))
        else:
            shipment_data=list(collection_shipment_data.find({"email":current_user["email"]}))
        return templates.TemplateResponse("myshipment.html", {"request": request,"shipment_data":shipment_data,"user":current_user})

    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    