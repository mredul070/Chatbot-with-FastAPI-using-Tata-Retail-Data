import uuid
from app.db.base_class import Base, Timestamp
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

class UserSession(Base):
    __tablename__ = 'user_sessions'
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey('users.id'))

    user = relationship("Users", back_populates="sessions")
    queries = relationship("UserQuery", back_populates="session")