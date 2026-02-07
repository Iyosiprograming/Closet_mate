import os
import shutil
import uuid
from fastapi import FastAPI, HTTPException, Depends, Header, status, UploadFile, File , Form
from sqlalchemy.orm import Session
from model import User, ClothingItem
from database import SessionLocal, get_db
from schema import UserCreate, UserLogin,  AiSuggestion
from password import hash_password, verify_password
from jwt import create_access_token, decode_access_token
from gemini import get_gemini_response
import uuid

UPLOAD_FOLDER = "./images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = FastAPI(title="Closet Mate")

# System prompt
SYSTEM_PROMPT = (
    "You are a professional fashion stylist. "
    "Suggest outfits based on the user’s occasion and existing wardrobe. "
    "Be creative, clear, and concise."
)

# Helper function 
def get_current_user(authorization: str = Header(..., alias="Authorization")):
    try:
        token = authorization.split(" ")[1]
        payload = decode_access_token(token)
        return payload["user_id"]
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )

# user regisrtation
@app.post("/create")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="400: User already registered")

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

# user login
@app.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
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


# insert clothes
@app.post("/upload")
def upload_outfit(
    name: str = Form(...),
    category: str = Form(...),
    color: str = Form(...),
    style: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    try:
        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            raise HTTPException(status_code=400, detail="File must be an image")

        # Save file with UUID
        ext = os.path.splitext(file.filename)[1]
        image_filename = f"{user_id}_{uuid.uuid4().hex}{ext}"
        image_path = os.path.join(UPLOAD_FOLDER, image_filename)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Short description
        short_desc = f"{name} - {color} {category} ({style})"

        # Save to DB
        new_clothe = ClothingItem(
            user_id=user_id,
            name=name,
            category=category,
            color=color,
            style=style,
            short_descripiton=short_desc,
            image_url=image_path
        )
        db.add(new_clothe)
        db.commit()
        db.refresh(new_clothe)

        return {"message": "Clothe added successfully", "id": new_clothe.id}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# AI outfit suggestion
@app.post("/suggestion")
async def get_suggestion(
    prompt: AiSuggestion,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    try:
        clothing_items = db.query(ClothingItem.id, ClothingItem.short_descripiton).filter(ClothingItem.user_id == user_id).all()
        if not clothing_items:
            raise HTTPException(status_code=404, detail="No clothing items found")

        items_text = ", ".join([f"{id}:{desc}" for id, desc in clothing_items])
        final_prompt = f"{SYSTEM_PROMPT}, {prompt.prompt}\nUser clothing items: {items_text}\nRespond only with the IDs of the suggested items as integers separated by commas."

        response_text = await get_gemini_response(final_prompt)

        # Convert AI response to integers
        try:
            suggested_ids = [int(x.strip()) for x in response_text.split(",") if x.strip().isdigit()]
        except ValueError:
            raise HTTPException(status_code=500, detail="AI returned invalid ID format")

        suggested_items = db.query(ClothingItem).filter(ClothingItem.id.in_(suggested_ids)).all()

        # Return the clothing items
        result = [
            {
                "id": item.id,
                "name": item.name,
                "category": item.category,
                "color": item.color,
                "style": item.style,
                "short_description": item.short_descripiton,
                "image_url": item.image_url
            }
            for item in suggested_items
        ]

        return {"suggested_items": result}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")