from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.dialects.postgresql import ARRAY
from ..db.database import Base

class FixNowUser(Base):
    __tablename__ = "fixnow_users"

    id = Column(Integer, primary_key=True, index=True)

    # Link with Keycloak
    keycloak_id = Column(String, unique=True, nullable=False)

    # Common fields
    full_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)   # optional for service users
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)      

    # Only for service providers
    service_type = Column(ARRAY(String))
    business_name = Column(String, nullable=True)
    address = Column(String, nullable=True)
    available_hours = Column(String, nullable=True)
    emergency_support = Column(Boolean, default=False)
    hourly_rate = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    experience = Column(String, nullable=True)
