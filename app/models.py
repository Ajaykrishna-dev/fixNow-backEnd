from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class ServiceProvider(Base):
    __tablename__ = "service_providers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    service_type = Column(String, nullable=False)
    business_name = Column(String)
    address = Column(String, nullable=False)
    available_hours = Column(String, nullable=False)
    emergency_support = Column(Boolean, default=False)
    hourly_rate = Column(Integer, nullable=False)
    description = Column(String)
    experience = Column(String)
