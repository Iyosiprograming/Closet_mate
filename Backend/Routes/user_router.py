from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.user_controller import create_user
from app.Schema.user_schema import CreateUser,CreateUserResponse

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/create",response_model=CreateUserResponse)
def create_user_endpoint(user:CreateUser, db:Session = Depends(get_db)):
    return create_user(user, db)


