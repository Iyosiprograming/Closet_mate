# main.py
import uvicorn
from fastapi import FastAPI
from database import Base, engine
from Routes.user_router import router as user_router

app = FastAPI(title="Closet Mate")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)