from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class CreateUserResponse(BaseModel):
    detail: dict

    class Config:
        orm_mode = True

class LoginUser(CreateUser):
    pass

class LoginUserResponse(CreateUserResponse):
    pass