from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles

from routers.signup import router as signup_router

from routers.login import router as login

from routers.shipment import router as shipment

from routers.forgetpswd import router as forgetpswd


from fastapi import FastAPI, Depends, Request, Response, status
from starlette.responses import RedirectResponse, HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordRequestForm


#To create instance of fastapi
#This app object is the main point of interaction of the application with the client browser. The uvicorn server uses this object to listen to client’s request.
app = FastAPI()

#To access the html folder
templates = Jinja2Templates(directory="html")

#To add css to html
app.mount("/static", StaticFiles(directory="static"), name="static")



#To include routers
app.include_router(signup_router)
app.include_router(login)
app.include_router(shipment)
app.include_router(forgetpswd)





