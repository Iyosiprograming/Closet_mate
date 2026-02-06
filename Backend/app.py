from fastapi import FastAPI, HTTPException, Depends, Header, status
from model import User, ClothingItem
from database import SessionLocal, get_db
from schema import UserCreate, UserLogin, OutfitUpload, AiSuggestion
from password import hash_password, verify_password
from jwt import create_access_token, decode_access_token

app = FastAPI(title="Closet Mate")


# Helper function 
def get_current_user(authorization: str = Header(..., alias="Authorization")):
    try:
        token = authorization.split(" ")[1]  
        payload = decode_access_token(token)  
        return payload['user_id']
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )


# Create a new user
@app.post("/create")
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already registered")

        new_user = User(
            username=user.username,
            email=user.email,
            password=hash_password(user.password)
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User created successfully", "user_id": new_user.id}


    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# User login
@app.post("/login")
def login_user(user: UserLogin, db: SessionLocal = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if not existing_user or not verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        access_token = create_access_token(
            data={"user_id": existing_user.id, "email": existing_user.email}
        )
        return {
            "message": "User logged in successfully",
            "user_id": existing_user.id,
            "token": access_token
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# Insert a clothing item
@app.post("/upload")
def upload_outfit(
    outfit: OutfitUpload,
    db: SessionLocal = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    try:
        short_desc = f"{outfit.name} - {outfit.color} {outfit.category} ({outfit.style})"
        new_clothe = ClothingItem(
            user_id=user_id,
            name=outfit.name,
            category=outfit.category,
            color=outfit.color,
            style=outfit.style,
            short_descripiton=short_desc
        )
        db.add(new_clothe)
        db.commit()
        db.refresh(new_clothe)
        return {"message": "Clothe added successfully", "id": new_clothe.id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# ai outfit suggestion
@app.post("/suggestion")
def get_suggestion(prompt: AiSuggestion, 
        db: SessionLocal = Depends(get_db),
        user_id:int = Depends(get_current_user)):
    try:
        clothing_item = db.query(ClothingItem.short_descripiton).first()
        if clothing_item:
            return {"short_description": clothing_item.short_descripiton}
        return {"short_description": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")