from pydantic import BaseModel,EmailStr
import datetime

class CreateUser(BaseModel):
    email:EmailStr
    password:str

class CreateUserResponse(BaseModel):
    message:str


class LoginUser(CreateUser):
    pass


class LoginUserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    