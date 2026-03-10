import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from Routers.user_router import router as user_router
from Routers.clothe_router import router as clothe_router
from Models.user_model import User
from Models.clothe_model import Clothe

Base.metadata.create_all(bind=engine)

app = FastAPI()

# include routers
app.include_router(user_router)
app.include_router(clothe_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)