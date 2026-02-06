from app import app
from database import Base, engine
import uvicorn
from model import User, ClothingItem 

Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)