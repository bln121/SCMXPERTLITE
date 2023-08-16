from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Request, HTTPException,Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
from fastapi.staticfiles import StaticFiles


from fastapi import APIRouter
from dotenv import load_dotenv
from config.config import SETTING

import bcrypt

import time

load_dotenv()

collection_users=SETTING.SIGNUP_COLLECTION

router = APIRouter()
templates = Jinja2Templates(directory="html")
#To add css to html
router.mount("/static", StaticFiles(directory="static"), name="static")




@router.post("/signup")
def signup(request: Request, username: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    try:
        #username must be six letters
        if len(username) < 6:
            raise HTTPException(status_code=400, detail="Username should be more than 6 characters")
         
        #To check either username already exists or not
        if collection_users.find_one({"username":username}):
            raise HTTPException("status_code=400", detail="Username already exists.")
        
        #Check either user is already registered with this email or not
        if collection_users.find_one({"email": email}):

            raise HTTPException(status_code=400, detail="Email already exists.")

        #To check either password and confirm password are same or not
        elif password != confirm_password:
            raise HTTPException(status_code=400, detail="Password and Confirm password do not match")
            
            #400 Bad Request: It indicates that the server could not understand the request due to invalid syntax, missing parameters, or validation error.
        else:
            #password encryption
            hashed_password = pswd_encrypt(password)
            #store data as json format to store it into db
            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password,
                "Role": "User"
            }
            #insertion of data
            collection_users.insert_one(user_data)
            return templates.TemplateResponse("signup.html", {"request": request, "success": "Account created successfully"})
           
    except HTTPException as e:
        #to display raised error on html page
        error_message = e.detail
        return templates.TemplateResponse("signup.html", {"request": request, "error": error_message})
        #return error_message
    except Exception as e:
        error_message = "An error occurred during signup. Please try again later."
        return templates.TemplateResponse("signup.html", {"request": request, "error": error_message})
    

    

    

#Password encryption
def pswd_encrypt(user_password):
    
    #password encription
    password = user_password.encode('utf-8')

    # Generate a salt (a random value used during hashing)
    salt = bcrypt.gensalt()

    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password, salt)
    return hashed_password
    





@router.get("/signup")
def show_signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})



   


