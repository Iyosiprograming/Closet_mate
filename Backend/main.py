import uvicorn
from fastapi import FastAPI
from database import Base, engine
from Routers import  user_router
from Models.user_model import User
from Models.clothe_model import Clothe

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user_router.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)