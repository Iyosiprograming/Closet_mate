from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Clothe(Base):
    __tablename__ = "clothes"
    id = Column(String, primary_key=True, nullable=False)
    user_id = Column(ForeignKey('user_id'),nullable=False)
    name = Column(String, nullable=True)
    color = Column(String, nullable=False)
    kind = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, datetime.utcnow)
    users = relationship("Users", back_populates="clothes")