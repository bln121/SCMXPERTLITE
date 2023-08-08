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
app = FastAPI()
templates = Jinja2Templates(directory="html")

#To add css to html
app.mount("/static", StaticFiles(directory="static"), name="static")




class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    Role: str



@app.exception_handler(HTTPException)
async def redirect_to_login(request: Request, exc: HTTPException):
    if exc.status_code == 401:
        return HTMLResponse("<script>window.location.href = '/';</script>")
    raise exc





app.include_router(signup_router)
app.include_router(login)
app.include_router(shipment)
app.include_router(forgetpswd)





@app.get("/signup")
async def get_signup(request: Request):
    return templates.TemplateResponse("signup.html",{"request":request})

@app.get("/gmail_authenticate")
async def gmail_authentication(request: Request):
    return templates.TemplateResponse("gmail_authenticate.html",{"request":request})




@app.get("/new_pswd")
async def new_pswd(request: Request):
    return templates.TemplateResponse("new_pswd.html", {"request": request})
