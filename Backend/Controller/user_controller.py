from fastapi import HTTPException, status, Response,Cookie
from sqlalchemy.orm import Session
from Models.user_model import User
from Schema.user_schema import UserCreate, UserCreateResponse, UserLogin, UserLoginResponse, MeResponse
from Services.password import hash_password, verify_password
from Services.jwt import create_access_token, decode_access_token, verify_access_token

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


def me_user(
    db: Session,
    access_token: str | None = Cookie(default=None)
):
    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    payload = decode_access_token(access_token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token payload"
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return MeResponse(
        id=user.id,
        email=user.email,
        created_at=user.created_at,
        message="User fetched successfully"
    )