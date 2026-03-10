from pydantic import BaseModel

class AddClothe(BaseModel):
    name: str | None = None
    color: str
    Kind: str
    description: str
    image_url: str
    
    class Config:
        from_attributes = True

class AddClotheResponse(BaseModel):
    status_code: int
    message: str
    detail: dict