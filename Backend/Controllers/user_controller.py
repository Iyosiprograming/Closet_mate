from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.model.user_model import users as User
from app.services.password import hash_password, verify_password
from app.services.jwt import create_access_token, verify_access_token
from app.schema import CreateUser,CreateUserResponse

def create_user(user:CreateUser,db: Session)->CreateUserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User Exists")
    new_user = User(
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return CreateUserResponse(
        message = "User Created Sucessfully"
    )