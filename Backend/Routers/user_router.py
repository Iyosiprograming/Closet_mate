from fastapi import APIRouter, Depends
from Controllers.user_controller import register_user
from Schema.user_schema import CreateUser, CreateUserResponse
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=CreateUserResponse)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    return register_user(user, db)