# main.py
import uvicorn
from fastapi import FastAPI
from database import Base, engine
from Routes.user_router import router as user_router
from Routes.clothe_router import router as clothe_router

app = FastAPI(title="Closet Mate")

Base.metadata.create_all(bind=engine)

app.include_router(user_router)
app.include_router(clothe_router)
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)