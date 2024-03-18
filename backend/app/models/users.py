import uuid
from app.db.base_class import Base, Timestamp
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class Users(Base, Timestamp):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String(25), unique=True, index=True, nullable=False)
    email = Column(String(256), nullable=False)
    password = Column(String(255), nullable=False)

    sessions = relationship("UserSession", back_populates="user")

