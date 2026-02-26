from fastapi import APIRouter, Depends,Response,Cookie
from sqlalchemy.orm import Session
from database import get_db
from Schema.clothe_schema import AddClothe, AddClotheResponse
from Controller.clothe_controller import add_clothe

router = APIRouter(prefix="/clothe", tags=["clothe"])

@router.post("/add", response_model=AddClotheResponse)
def add_clothe_endpoint(clothe: AddClothe, db: Session = Depends(get_db),access_token: str | None = Cookie(default=None, include_in_schema=False)):
    return add_clothe(clothe=clothe, db=db,access_token=access_token)