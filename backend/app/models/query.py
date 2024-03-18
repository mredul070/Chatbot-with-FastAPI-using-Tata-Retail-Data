import uuid
from app.db.base_class import Base, Timestamp
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class UserQuery(Base):
    __tablename__ = 'user_queries'
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    SessionID = Column(UUID, ForeignKey('user_sessions.id'))
    QueryText = Column(String)
    ResponseText = Column(String)

    session = relationship("UserSession", back_populates="queries")
