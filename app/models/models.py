from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    username: str
    hashed_password: str


class SignupData(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    Role: str


class Shipment(BaseModel):
    email:str
    shipment_number:int
    container_number:int
    route_details:str
    goods_type:str
    device_name:str
    delivery_date:str
    po_number:int
    delivery_no:int
    NDC_number:int
    Batch_id:int
    serial_number:int
    shipment_desc: Optional[str] = None