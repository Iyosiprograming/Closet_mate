from pydantic import BaseModel, EmailStr
from datetime import datetime

class AddClothe(BaseModel):
    name: str
    category: str
    color: str
    size: str
    kind: str
    image_url: str | None

class AddClotheResponse(BaseModel):
    id: int
    name: str
    category: str
    color: str
    size: str
    kind: str
    image_url: str
    created_at: datetime
    message:str

    model_config = {
        "from_attributes": True
    }

class DeleteClotheResponse(BaseModel):
    clothe_id: int
    name: str
    category: str
    color: str
    size: str
    kind: str
    image_url: str
    created_at: datetime
    message: str
