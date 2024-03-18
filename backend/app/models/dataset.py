import uuid
from app.db.base_class import Base, Timestamp
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class Dataset(Base, Timestamp):
    __tablename__ = 'dataset'
    __table_args__ = {'extend_existing': True}
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    CustomerID = Column(Integer, nullable=False)
    StockCode = Column(String(256), nullable=False)
    Description = Column(String(512), nullable=False)
    UnitPrice = Column(Float, nullable=False)
    InvoiceNo = Column(Integer, nullable=False)
    InvoiceDate = Column(DateTime, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Country = Column(String, nullable=False)

