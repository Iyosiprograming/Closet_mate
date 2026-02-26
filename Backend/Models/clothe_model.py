from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Clothe(Base):
    __tablename__ = "clothes"
    id = Column(integer, primary_key=True,index=True,nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    category = Column(String, nullable=False)
    color = Column(String, nullable=False)
    size = Column(String, nullable=False)
    kind = Column(String,nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="clothes")