from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models.user_model import User
from Services.password import hashPassword
from Schema.user_schema import CreateUser, CreateUserResponse

def register_user(user: CreateUser, db: Session) -> CreateUserResponse:
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    hashed_password = hash(user.password)
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