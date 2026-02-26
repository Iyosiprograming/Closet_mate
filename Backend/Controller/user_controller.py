from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models.user_model import User
from Schema.user_schema import UserCreate, UserCreateResponse
from Services.password import hash_password

def create_user(user: UserCreate, db: Session):

    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    # Hash password
    hashed_password = hash_password(user.password)

    new_user = User(
        email=user.email,
        password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  

    return UserCreateResponse(
        id=new_user.id,            
        email=new_user.email,
        created_at=new_user.created_at,
        message="User created successfully"
    )

    #ott$hM8N8AH-T3B2_rjfRC8aInJ55s87GLCF0eHAKyEPwNs