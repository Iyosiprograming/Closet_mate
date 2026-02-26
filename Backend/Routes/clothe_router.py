from fastapi import APIRouter, Depends,Response,Cookie
from sqlalchemy.orm import Session
from database import get_db
from Schema.clothe_schema import AddClothe, AddClotheResponse,DeleteClotheResponse,GetClotheResponse
from Controller.clothe_controller import add_clothe,delete_clothe,get_all_clothe

router = APIRouter(prefix="/clothe", tags=["clothe"])

@router.post("/add", response_model=AddClotheResponse)
def add_clothe_endpoint(clothe: AddClothe, db: Session = Depends(get_db),access_token: str | None = Cookie(default=None, include_in_schema=False)):
    return add_clothe(clothe=clothe, db=db,access_token=access_token)

@router.delete("/delete/{clothe_id}", response_model=DeleteClotheResponse)
def delete_clothe_endpoint(clothe_id: int, db: Session = Depends(get_db),access_token: str | None = Cookie(default=None, include_in_schema=False)):
    return delete_clothe(clothe_id=clothe_id, db=db,access_token=access_token)

@router.get("/all", response_model=list[GetClotheResponse])
def get_all_clothe_endpoint(db: Session = Depends(get_db),access_token: str | None = Cookie(default=None, include_in_schema=False))->list[GetClotheResponse]:
    return get_all_clothe(db=db,access_token=access_token)