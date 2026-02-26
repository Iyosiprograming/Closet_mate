from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from Models.user_model import User
from Schema.user_schema import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse
from Services.password import hash_password, verify_password
from Services.jwt import create_access_token

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


def login_user(user:UserLogin, response: Response, db: Session):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": existing_user.email})
    response.set_cookie(
        key="access_token",
        value = access_token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=3600
    )

    return UserLoginResponse(
        id=existing_user.id,
        email=existing_user.email,
        created_at = existing_user.created_at,
        message = "User logged in successfully"
    )