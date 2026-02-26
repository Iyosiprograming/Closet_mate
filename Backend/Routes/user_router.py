from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from Schema.user_schema import UserCreate, UserCreateResponse
from Controller.user_controller import create_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserCreateResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)