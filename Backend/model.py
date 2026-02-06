from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

# model for the user
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)
    clothing_items = relationship("ClothingItem", back_populates="user")

# data model for the user clothes
class ClothingItem(Base):
    __tablename__ = "clothing_items"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=True)
    category = Column(String, nullable=False)
    color = Column(String, nullable=False)
    style = Column(String, nullable=False)
    user = relationship("User", back_populates="clothing_items")