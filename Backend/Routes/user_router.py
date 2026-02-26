from fastapi import APIRouter, Depends,Response,Cookie
from sqlalchemy.orm import Session
from database import get_db
from Schema.user_schema import UserCreate, UserCreateResponse,UserLogin,UserLoginResponse,MeResponse
from Controller.user_controller import create_user,login_user,me_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/create", response_model=UserCreateResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(user, db)

@router.post("/login",response_model=UserLoginResponse)
def login_user_endpoint(user: UserLogin, response: Response, db: Session = Depends(get_db)):
    return login_user(user, response, db)
@router.get("/me", response_model=MeResponse)
def me_user_endpoint(
    db: Session = Depends(get_db),
    access_token: str | None = Cookie(default=None, include_in_schema=False)
):
    return me_user(db=db, access_token=access_token)