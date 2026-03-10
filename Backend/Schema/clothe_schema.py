from pydantic import BaseModel
from typing import List
class AddClothe(BaseModel):
    name: str | None = None
    color: str
    category: str
    description: str
    image_url: str
    
    class Config:
        from_attributes = True

class AddClotheResponse(BaseModel):
    status_code: int
    message: str
    detail: dict

class AllClotheResponse(AddClotheResponse):
    clothes: List[AddClothe]

class AiSuggestion(BaseModel):
    user_prompt: str

class AiSuggestionResponse(BaseModel):
    status_code: int
    message: str
    detail: dict