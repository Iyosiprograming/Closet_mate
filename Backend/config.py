from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = "mysecretkey123"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60