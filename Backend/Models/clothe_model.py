from sqlalchemy import Column, String, UUID, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Clothe(Base):
    __tablename__ = "clothe"
    id = Column(UUID (as_uuid=True), primary_key=True,default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    name = Column(String, nullable=True)
    color = Column(String, nullable=False)
    Kind = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="clothe")