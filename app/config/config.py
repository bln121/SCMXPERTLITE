import os
import pymongo
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Settings:
    """creating environmental variables"""
    TITLE: str = "SCMXpertLite"
    DESCRIPTION: str = """SCMXpertLite  created using FastAPI"""
    PROJECT_VERSION: str = "0.0.1"
    MONGODB_USER = os.getenv("mongodb_user")
    MONGODB_PASSWORD = os.getenv("mongodb_password")
    CLIENT = pymongo.MongoClient(os.getenv("mongodbUri"))
    DB = CLIENT['shipment_db']
    SIGNUP_COLLECTION = DB['shipment_users']
    SHIPMENT_COLLECTION = DB['shipment_data']
    DATA_STREAM = DB["stream_data"]
    SECRET_KEY: str = "secret-key"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30 # in mins
    COOKIE_NAME = "access_token"
    HOST = os.getenv("host")
    PORT = (os.getenv("port"))

SETTING = Settings()
