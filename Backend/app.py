from fastapi import FastAPI, HTTPException , Depends , Header , status
from model import User, ClothingItem
from database import SessionLocal, Base, get_db
from schema import UserCreate , UserLogin , OutfitUpload
from password import hash_password, verify_password
from jwt import create_access_token , decode_access_token

app = FastAPI(title="Closet Mate")


# helper function
def get_current_user(authorization: str = Header(..., alias="Authorization")):
    try:
        token = authorization.split(" ")[1]  
        payload = decode_access_token(token)  
        user_id = payload['user_id']        
        return user_id
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token"
        )

    
# create a new user
@app.post("/create")
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    try:
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
    except Exception  as e:
        return {"message":"Server error while regisrtation", "error":e}


# user login
@app.post("/login")
def login_user(user:UserLogin, db:SessionLocal = Depends(get_db)):
    try:
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

    except Exception  as e:
        return {"message":"Server error while regisrtation", "error":e}

# inset the clothe to clothe_item
@app.post("/upload")
def upload_outfit(outfit:OutfitUpload, db:SessionLocal = Depends(get_db), user_id:int = Depends(get_current_user)):
    try:
        new_clothe = ClothingItem(
            user_id = user_id,
            name = outfit.name,
            category = outfit.category,
            color = outfit.color,
            style = outfit.style
        )
        db.add(new_clothe)
        db.commit()
        db.refresh(new_clothe)
        return {
            "message":"clothe added sucessfully",
            "id": new_clothe.id}
    except Exception  as e:
        return {"message":"Server error while regisrtation", "error":e}

# get a suggestion from the ai
