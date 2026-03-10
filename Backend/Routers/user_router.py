from fastapi import APIRouter, Depends,Response, status
from Controllers.user_controller import register_user, login_user,me
from Schema.user_schema import CreateUser, CreateUserResponse,LoginUser,LoginUserResponse,MeResponse
from Services.jwt import get_current_user
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=CreateUserResponse , status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: CreateUser, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login", response_model=LoginUserResponse, status_code=status.HTTP_200_OK)
def login_user_endpoint(user:LoginUser, response:Response, db: Session = Depends(get_db)):
        return login_user(user, response, db)

@router.get("/me", response_model=MeResponse, status_code=status.HTTP_200_OK)
def me_endpoint(user_id: str = Depends(get_current_user),db: Session = Depends(get_db)):
    return me(user_id, db)