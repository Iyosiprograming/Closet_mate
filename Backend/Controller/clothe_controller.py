from fastapi import HTTPException, status, Response,Cookie
from sqlalchemy.orm import Session
from Models.clothe_model import Clothe
from Models.user_model import User
from Schema.clothe_schema import AddClothe, AddClotheResponse,DeleteClotheResponse,GetClotheResponse
from Services.jwt import decode_access_token

def add_clothe(clothe: AddClothe, db: Session,access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(access_token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_clothe = Clothe(
        user_id=user.id,
        name=clothe.name,
        category=clothe.category,
        color=clothe.color,
        size=clothe.size,
        kind=clothe.kind,
        image_url=clothe.image_url
    )
    db.add(new_clothe)
    db.commit()
    db.refresh(new_clothe)

    return AddClotheResponse(
        id=new_clothe.id,
        name=new_clothe.name,
        category=new_clothe.category,
        color=new_clothe.color,
        size=new_clothe.size,
        kind=new_clothe.kind,
        image_url=new_clothe.image_url,
        created_at=new_clothe.created_at,
        message="Clothe added successfully"
    )

def delete_clothe(clothe_id: int, db: Session,access_token: str | None = Cookie(default=None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(access_token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    clothe = db.query(Clothe).filter(Clothe.id == clothe_id, Clothe.user_id == user.id).first()
    if not clothe:
        raise HTTPException(status_code=404, detail="Clothe not found")
    
    db.delete(clothe)
    db.commit()

    return DeleteClotheResponse(
        clothe_id=clothe.id,
        name=clothe.name,
        category=clothe.category,
        color=clothe.color,
        size=clothe.size,
        kind = clothe.kind,
        image_url = clothe.image_url,
        created_at = clothe.created_at,
        message = "deleted succesfully"
    )
        
def get_all_clothe(db: Session,access_token: str | None = Cookie(default=None))->list[GetClotheResponse]:
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    payload = decode_access_token(access_token)
    email = payload.get("sub")

    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    clothes = db.query(Clothe).filter(Clothe.user_id == user.id).all()
    
    return [
            GetClotheResponse(
                id=c.id,
                name=c.name,
                category=c.category,
                color=c.color,
                size=c.size,
                kind=c.kind,
                image_url=c.image_url,
                created_at=c.created_at
            )
            for c in clothes
        ]