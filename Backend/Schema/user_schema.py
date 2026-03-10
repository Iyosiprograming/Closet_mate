from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class CreateUserResponse(BaseModel):
    detail: dict

    class Config:
        from_attributes = True

class LoginUser(CreateUser):
    pass

class LoginUserResponse(CreateUserResponse):
    pass

class MeResponse(CreateUserResponse):
    pass