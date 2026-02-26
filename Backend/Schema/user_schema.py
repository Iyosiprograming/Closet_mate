from pydantic import BaseModel, EmailStr
from datetime import datetime
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserCreateResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    message:str

model_config = {
        "from_attributes": True
    }