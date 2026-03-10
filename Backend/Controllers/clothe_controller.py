import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models.clothe_model import Clothe
from Schema.clothe_schema import AddClothe, AddClotheResponse


def add_clothe(clothe: AddClothe, user_id: uuid.UUID, db: Session):

    new_clothe = Clothe(
        name=clothe.name,
        color=clothe.color,
        Kind=clothe.Kind,
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
            "Kind"  : new_clothe.Kind,
            "description": new_clothe.description,
            "image_url": new_clothe.image_url,
            "user_id": str(new_clothe.user_id),
            "created_at": new_clothe.created_at}
    )