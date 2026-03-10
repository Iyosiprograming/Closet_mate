import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models.clothe_model import Clothe
from Schema.clothe_schema import AddClothe, AddClotheResponse, AllClotheResponse


def add_clothe(clothe: AddClothe, user_id: uuid.UUID, db: Session):

    new_clothe = Clothe(
        name=clothe.name,
        color=clothe.color,
        category=clothe.category,
        description=clothe.description,
        image_url=clothe.image_url,
        user_id=uuid.UUID(user_id)
    )

    db.add(new_clothe)
    db.commit()
    db.refresh(new_clothe)

    return AddClotheResponse(
        status_code=status.HTTP_201_CREATED,
        message="Clothe added successfully",
        detail={
            "clothe_id": new_clothe.id,
            "name": new_clothe.name,
            "color": new_clothe.color,
            "category"  : new_clothe.category,
            "description": new_clothe.description,
            "image_url": new_clothe.image_url,
            "user_id": str(new_clothe.user_id),
            "created_at": new_clothe.created_at}
    )

def get_all_clothe(user_id: uuid.UUID, db: Session):
    user_id = uuid.UUID(user_id)
    clothes = db.query(Clothe).filter(Clothe.user_id == user_id).all()

    if not clothes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Clothes not found"
        )

    clothes_list = [
        {
            "clothe_id": str(c.id),
            "name": c.name,
            "color": c.color,
            "category": c.category,
            "description": c.description,
            "image_url": c.image_url,
            "user_id": str(c.user_id),
            "created_at": c.created_at
        }
        for c in clothes
    ]

    return AllClotheResponse(
        status_code=status.HTTP_200_OK,
        message="Clothes fetched successfully",
        detail={},
        clothes=clothes_list
    )