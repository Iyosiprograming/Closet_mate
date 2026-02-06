from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = "mysecretkey123"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = os.getenv("GEMINI_URL")