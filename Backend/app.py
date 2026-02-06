from fastapi import FastAPI, HTTPException , Depends
from model import User, ClothingItem
from database import SessionLocal, Base, get_db
from schema import UserCreate , UserLogin
from password import hash_password, verify_password
from jwt import create_access_token , decode_access_token
app = FastAPI(title="Closet Mate")

# create a new user
@app.post("/create")
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    new_user = User(
        username = user.username,
        email = user.email,
        password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user_id": new_user.id}

# user login
@app.post("/login")
def login_user(user:UserLogin, db:SessionLocal = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid Credintial")

    verify_password(user.password, existing_user.password)
    if not verify_password:
        raise HTTPException(status_code=400, detail="Invalid Credintial")

    access_token = create_access_token(data={"user_id": existing_user.id, "email": existing_user.email})

    return{
        "message":"User Loged in sucessfully",
        "user_id": existing_user.id,
        "token": access_token
    }