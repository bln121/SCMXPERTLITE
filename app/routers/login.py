from typing import Dict, List, Optional
from fastapi import Request
from fastapi.security import OAuth2, OAuth2PasswordRequestForm
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Form, Request, HTTPException, status, Depends, Response, APIRouter
from fastapi.security.utils import get_authorization_scheme_param
import datetime as dt
from jose import JWTError, jwt
from passlib.context import CryptContext



from fastapi.logger import logger
from fastapi.responses import HTMLResponse, RedirectResponse

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates




from pydantic import BaseModel, EmailStr
from fastapi import FastAPI, Request, HTTPException,responses,Form
from fastapi.responses import HTMLResponse
#from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
#from fastapi.staticfiles import StaticFiles

from starlette.status import HTTP_302_FOUND, HTTP_401_UNAUTHORIZED
from fastapi import APIRouter
#from routers.database import collection_users,collection_stream_data
from models.models import User
from dotenv import load_dotenv
from config.config import SETTING

load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="html")

#To add css to html
router.mount("/static", StaticFiles(directory="static"), name="static")


collection_users=SETTING.SIGNUP_COLLECTION

collection_stream_data=SETTING.DATA_STREAM


router = APIRouter()

#  for password encrypt and decrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

#To verify either user pswd and given pswd both are same or not
def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


'''
    HS256 (HMAC-SHA256) is a widely used symmetric encryption algorithm that falls under the category of hash-based 
    message authentication codes (HMAC). It's primarily used for creating digital signatures and verifying the integrity 
    and authenticity of data.
'''



#Fetches data from the login user and stores data 
class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.login_user: Optional[str] = None
        self.login_password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.login_user = form.get("user_email")
        self.login_password = form.get("user_password")
        #print(self.login_user)

    async def is_valid(self):
        form = await self.request.form()
        # authenticate_user(self.login_user, self.login_password)
        captcha_response = form.get("g-recaptcha-response")
        if not captcha_response:
            self.errors.append("Please click the Google reCAPTCHA.")
        if not self.errors:
            return True
        return False  
     

#OAuth2PasswordBearerWithCookie in herits OAuth2 parent class
class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str, #A required string parameter representing the URL where the token can be obtained.
        scheme_name: Optional[str] = None, #name of the authentication scheme.
        scopes: Optional[Dict[str, str]] = None, # dictionary parameter representing the scopes associated with the authentication.
        description: Optional[str] = None,
        auto_error: bool = True,  # A boolean parameter with a default value of True. It determines whether errors related to authentication should be raised automatically.
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})#Creating instance of OAuthFlowsModel
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )#It passes the defined parameters (flows, scheme_name, description, and auto_error) to the parent class constructor to initialize the inherited properties and behavior.

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get(SETTING.COOKIE_NAME)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return param


oauth2_schema = OAuth2PasswordBearerWithCookie(tokenUrl="token")#t allows you to create instances of this class with specific configurations for handling OAuth2-based authentication with cookies.


#To create access token

def create_access_token(data: Dict) -> str:#data contains user's data which is bought from shipment_users
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=SETTING.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, SETTING.SECRET_KEY, algorithm=SETTING.ALGORITHM
    )
    return encoded_jwt



#To fetch current user
def get_user(email: str) -> User:
    user = collection_users.find_one({"email": email})
    #print("user is ",user)
    if user:
        return user

#To check either user is present in db or not
def authenticate_user(email: str, plain_password: str) -> User:
    user = get_user(email)
    #print("user at auth",user)
    if not user:
        raise HTTPException(status_code=404, detail="Invalid mail id/Please signup before login")
    if not verify_password(plain_password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    return user


#Decode token to get user data
def decode_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
    )
    token = str(token).replace("Bearer", "").strip()

    try:
        payload = jwt.decode(
            token, SETTING.SECRET_KEY, algorithms=[SETTING.ALGORITHM]
        )
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username)
    return user

'''
    A cookie is a small piece of data that a web server sends to a user's web browser. The browser stores this data and 
    includes it in subsequent requests back to the server. Cookies are used to remember user-specific information or to 
    track user activity across different pages and sessions on a website. 
'''


def get_current_user_from_token(token: str = Depends(oauth2_schema)) -> User:
    #   Get the current user from the cookies in a request.
    user = decode_token(token)
    return user


def get_current_user_from_cookie(request: Request) -> User:
    #     Get the current user from the cookies in a request.
    
    token = request.cookies.get(SETTING.COOKIE_NAME)
    user = decode_token(token)
    return user
    

#Authentication and creating access token
@router.post("token")
def login_for_access_token(
    response: Response, form_data: OAuth2PasswordRequestForm = Depends()
) -> Dict[str, str]:
    '''

    form_data: OAuth2PasswordRequestForm = Depends(): This parameter is of type OAuth2PasswordRequestForm, 
    which presumably holds the user's login credentials. It's being assigned a default value by calling Depends(), 
    which is a FastAPI function used to declare dependencies. This suggests that this function might be using FastAPI's 
    dependency injection mechanism to automatically populate form_data with the appropriate values.
'''
    # Authenticate the user with the provided credentials
    user = authenticate_user(form_data.login_user, form_data.login_password)
    try:
        if not user:
            # If the user is not authenticated, raise an HTTPException with 401 status code
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not registered"
            )

        # Create an access token for the authenticated user
        #here I am using user's email to create access token
        access_token = create_access_token(data={"username": user["email"]})
        #print(access_token)

        # httponly is set to True, it means that the cookie can only be accessed and modified by the server, and it cannot be accessed by client-side scripts (e.g., JavaScript).
        response.set_cookie(
            key=SETTING.COOKIE_NAME, value=f"Bearer {access_token}", httponly=True
        )
        # Return the access token and token type in a dictionary
        return {SETTING.COOKIE_NAME: access_token, "token_type": "bearer"}

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input data"
        )
    except TypeError:
        #  If an exception occurs, raise an HTTPException with a 500 status code and a generic error message
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error",
        )
    except (ConnectionError, TimeoutError):
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Could not connect to authentication server",
        )




pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# serves the login form page.
@router.get("/login", response_class=HTMLResponse)
def login_view(request: Request):
    return templates.TemplateResponse(
        "login.html", {"request": request}, status_code=200
    )


#  Handles the login form submission.


@router.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    #verigies either captcha is clicked or not
    if await form.is_valid():
        try:
            # It validates the form data and generates a new access token if it is valid,
            # then redirects to the dashboard page.
            response = RedirectResponse("/dash1", status.HTTP_302_FOUND)
            login_for_access_token(response=response, form_data=form)
            form.__dict__.update(msg="")
            return response
           
            

        except HTTPException as e:
            # Return 401 Unauthorized if the user is not authenticated or the form data is invalid.
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "message": e.detail},
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        


        except ValueError:
            # Return 400 Bad Request if the input data is invalid.
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "alert": "Invalid input data"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            # Return 500 Internal Server Error if any other unexpected exception occurs.
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "alert": "Internal server error"},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "captcha_error": form.errors[0] if form.errors else ""},
        status_code=200,
    )
        
#----------------------------------------get_dashboard--------------------------------------------------------#
@router.get("/dash1")
async def dashboard(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            return RedirectResponse(url="/login")
        else:
            #print("current_user",current_user)
            return templates.TemplateResponse("dash1.html", {"request": request, "user": current_user})
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")



        
#--------------------------------------------------------myaccount-------------------------------------------#

@router.get("/myaccount")
async def myaccount(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            # raise HTTPException(status_code=401, detail="You must be logged in to access this page.")
            return RedirectResponse(url="/login")
        else:
            #print("current_user",current_user)
            return templates.TemplateResponse("myaccount.html", {"request": request, "user": current_user})
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")




#--------------------------------------------------------data stream ----------------------------------------#

@router.get("/data_stream")
async def data_stream(request: Request, current_user: User = Depends(get_current_user_from_cookie)):
    try:
        if current_user is None:
            return RedirectResponse(url="/login")
        
        elif ((current_user['Role']).lower()=='admin' or (current_user['Role'])=='Super admin'):
            return templates.TemplateResponse("data_stream.html", {"request": request, "user": current_user})
        
        else:
            #print("current_user",current_user)
            name=current_user["username"]
           
            return templates.TemplateResponse("dash1.html", {"request": request, "message": f"!! {name} is not authorized to access the device data.","user":current_user})
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#---------------------------------------post data_stream----------------------------------------------------#

@router.post("/data_stream")
async def data_stream_post(request: Request, current_user: User = Depends(get_current_user_from_cookie),device_id :int =Form(...)):
     #print(device_id)
    try:
        if current_user is None:
            # raise HTTPException(status_code=401, detail="You must be logged in to access this page.")
            return RedirectResponse(url="/login")
        elif not isinstance(device_id,int):
            raise Exception("invalid option")
       
        elif ((current_user['Role']).lower()=='admin' or (current_user['Role'])=='Super admin'):
            
            result=list(collection_stream_data.find({"Device_Id":device_id}))
            #print(result)
            return templates.TemplateResponse("data_stream.html", {"request": request, "user": current_user,"stream_data":result})
        else:
            #print("current_user",current_user)
            name=current_user["username"]
            return templates.TemplateResponse("dash1.html", {"request": request, "message": f"!! {name} is not authorized to access the device data.","user":current_user})
    
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")



#-------------------------------------------get homepage------------------------------------------------------#
@router.get("/", response_class=HTMLResponse)
def get_homepage(request:Request):
    return templates.TemplateResponse("homepage.html", {"request": request})

#------------------------------------------get user_management-----------------------------------------------#

@router.get("/user_manage")
def get_user_manage(request: Request, current_user : User=Depends(get_current_user_from_cookie)):
    return templates.TemplateResponse("user_management.html", {"request":request})


#---------------------------------------post user_management------------------------------------------------#

@router.post("/user_manage")
def post_user_manage(request: Request, current_user : User=Depends(get_current_user_from_cookie),username:str = Form(),user_role :str = Form()):
    try:
        if collection_users.find_one({"username":username}):
            if current_user["Role"]=="Super admin":
                # user_role=user_role.capitalize
                result = collection_users.update_one({"username":username}, { '$set': { 'Role': user_role} })
                return templates.TemplateResponse("user_management.html",{"request":request, "success":"Updated Successfully."})
            else:
                return templates.TemplateResponse("user_management.html",{"request":request, "message":"Only Super admins can change user role."})
        else:
            return templates.TemplateResponse("user_management.html",{"request":request,"message":"Please enter valid username."})

    except KeyError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")

#------------------------logout------------------------------------------------------------------------------#

@router.get("/logout", response_class=HTMLResponse)
def logout():
    try:
        response = RedirectResponse(url="/")
        response.delete_cookie(SETTING.COOKIE_NAME)
        # response.delete_cookie(settings.COOKIE_NAME)
        return response
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")



