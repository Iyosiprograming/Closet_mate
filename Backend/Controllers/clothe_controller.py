import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from Models.clothe_model import Clothe
from Models.user_model import User
from Schema.clothe_schema import AddClothe, AddClotheResponse, AllClotheResponse,AiSuggestion,AiSuggestionResponse
from Services.ai_suggestion import get_suggestion

def add_clothe(clothe: AddClothe, user_id: uuid.UUID, db: Session):
    short_description = f"{clothe.name}, {clothe.color}, {clothe.category},{clothe.description}"
    new_clothe = Clothe(
        name=clothe.name,
        color=clothe.color,
        category=clothe.category,
        description=clothe.description,
        short_description = short_description,
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



async def suggestion(clothe: AiSuggestion, user_id: str, db: Session):
    user_id = uuid.UUID(user_id)

    existing_user = db.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_clothe = db.query(Clothe.short_description).filter(
        Clothe.user_id == user_id
    ).first()

    if not existing_clothe:
        raise HTTPException(status_code=404, detail="Clothe not found")

    short_description = existing_clothe[0]

    prompt = f"""
    Give me an outfit idea.

    Occasion: {clothe.user_prompt}

    My closet:
    {short_description}
    """

    result = await get_suggestion(prompt)

    return AiSuggestionResponse(
        status_code=200,
        message="Suggestion fetched successfully",
        detail=result
    )