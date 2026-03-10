from fastapi import HTTPException, status, Cookie, Response
from sqlalchemy.orm import Session
from Models.user_model import User
from Services.password import hashPassword, verifyhashPassword
from Services.jwt import create_access_token, verify_token
from Schema.user_schema import CreateUser, CreateUserResponse,LoginUser,LoginUserResponse

def register_user(user: CreateUser, db: Session) -> CreateUserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    hashed_password = hashPassword(user.password)
    new_user = User(
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return CreateUserResponse(
        detail={
            "user_id": new_user.id,
            "email": new_user.email,
            "status_code": status.HTTP_201_CREATED,
            "message": "User created successfully"
        }
    )

def login_user(user:LoginUser, response:Response, db:Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")
    if not verifyhashPassword(user.password, existing_user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credentials")

    access_token = create_access_token({"user_id":str(existing_user.id)})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        samesite="lax"
    )
    return LoginUserResponse(
        detail={
            "user_id": str(existing_user.id),
            "email": existing_user.email,
            "status_code": status.HTTP_200_OK,
            "message": "User logged in successfully"
        }
    )
