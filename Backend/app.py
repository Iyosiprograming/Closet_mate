from fastapi import FastAPI, HTTPException , Depends
from model import User, ClothingItem
from database import SessionLocal, Base, get_db
from schema import UserCreate
from password import hash_password, verify_password
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