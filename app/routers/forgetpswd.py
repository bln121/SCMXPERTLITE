from fastapi import FastAPI, HTTPException,Depends
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Request, HTTPException,responses,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles

from fastapi import APIRouter

#from routers.database import collection_users
from models.models import User
from routers.login import get_current_user_from_cookie
from config.config import SETTING

from dotenv import load_dotenv


#importing packages to send otp to email
import random
import smtplib
import string


import bcrypt



load_dotenv()
router = APIRouter()
templates = Jinja2Templates(directory="html")
#To add css to html
router.mount("/static", StaticFiles(directory="static"), name="static")

collection_users=SETTING.SIGNUP_COLLECTION

#Global variable declarations
receiver_email=""

otp = None

@router.post("/forgetpswd")
async def forget_password(request: Request,user_email: str=Form(...)):
    global receiver_email
    receiver_email = user_email
    try:
        if not collection_users.find_one({"email": user_email}):
            message = "Email doesn't exist"
            return templates.TemplateResponse("forgetpswd.html", {"request": request, "message": message})
        else:
            global otp
            otp = generate_otp()
        # otp="bln"#comment this
            connect_server = smtp_connection(otp, receiver_email)# remove comment
            return templates.TemplateResponse("gmail_authenticate.html", {"request": request})

    except KeyError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#--------------------------------------------get_forgetpswd-----------------------------------#

@router.get("/forgetpswd")
async def forget_paswd_show(request: Request):
    return templates.TemplateResponse("forgetpswd.html", {"request":request})

                        

#---------------------------------------#gmail authentication------------- ---------------------#
@router.post("/gmail_authenticate")
async def gmail_authentication(request: Request,user_otp : str =Form(...)):
    global otp
    try:
        print("generated pass",user_otp)
        if otp == user_otp:
            return templates.TemplateResponse("new_pswd.html", {"request": request})#if generated and user_otp matches goes new password generation page
        else:
            return templates.TemplateResponse("gmail_authenticate.html", {"request": request, "otp_error": "Incorrect OTP, please enter a valid OTP"})
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

    

#Connect to smtp server
def smtp_connection(otp,receiver_email):
    server=smtplib.SMTP('smtp.gmail.com',587)
    #adding TLS security 
    server.starttls()
    email="lakshminarayanabachu802@gmail.com"
    password="qwaccvzyenijymwh"
    server.login(email,password)
    msg='Hello, Your OTP is '+str(otp)
    #sender='lakshminarayanabachu802@gmail.com'  #write email id of sender
    receiver=receiver_email #write email of receiver
    server.sendmail(email,receiver,msg)
    server.quit()



#Generates otp
def generate_otp(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



#-----------------------------new password----------------------------------------------------#

@router.post("/new_pswd")
def update_password(request: Request,new_password :str=Form(...),confirm_password : str=Form(...)):
    
    #Fetch data from db
    get_user_data=collection_users.find_one({"email":receiver_email})
  
    msg=  checkpswd(get_user_data["password"], new_password, request)
 
    try:
        if msg=="previous password":
            return templates.TemplateResponse("new_pswd.html", {"request": request, "error_msg": "New password must be different to previously used password."})
        elif msg=="different password":
             
             if(new_password!=confirm_password):#check pswd and confirm pswd are same or not
                return templates.TemplateResponse("new_pswd.html", {"request": request, "error_msg": "New password and confirm password doesn't match"})

             hashed_pswd=pswd_encrypt(new_password)
             update_result = collection_users.update_one({"email": receiver_email},{"$set": {"password": hashed_pswd}})
             
             return templates.TemplateResponse("pswd_succesful.html", {"request": request})
             #raise Exception("Password is updated successfully!")      
        
        
    
    except Exception as updated:
        return templates.TemplateResponse("new_pswd.html", {"request": request, "updated_msg": updated})
    
        
    



#To check either previous password and new password same or not
def checkpswd( passw, new_passw,request: Request):#passw in db, user pswd given in login form
    # Retrieve the hashed password from the database
    stored_hashed_password = passw

    # User's provided password
    provided_password = new_passw.encode('utf-8')

    # Compare the provided password with the stored hashed password
    if bcrypt.checkpw(provided_password, stored_hashed_password):
        message="previous password"
        
        
    else:
        message="different password"
        

    #return templates.TemplateResponse("login.html", {"request": request, "message":message})
    return message


def pswd_encrypt(new_password):
    #password encription
    password = new_password.encode('utf-8')

    # Generate a salt (a random value used during hashing)
    salt = bcrypt.gensalt()

    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password


@router.get("/pswd_successful")
def show_pswd_successful(request:Request):
    return templates.TemplateResponse("pswd_succesful.html", {"request": request})