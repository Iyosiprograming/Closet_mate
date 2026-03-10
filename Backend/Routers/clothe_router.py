from fastapi import APIRouter, Depends,Response, status
from Controllers.clothe_controller import add_clothe
from Schema.clothe_schema import AddClothe, AddClotheResponse
from Services.jwt import get_current_user
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clothes", tags=["clothes"])

@router.post("/", response_model=AddClotheResponse, status_code=status.HTTP_201_CREATED)
def add_clothe_endpoint(clothe: AddClothe, user_id: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return add_clothe(clothe, user_id, db)