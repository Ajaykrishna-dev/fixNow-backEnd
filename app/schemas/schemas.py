from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Base schema for all users
class FixNowUserBase(BaseModel):
    full_name: str = Field(alias="fullName")
    email: EmailStr
    role: str  # "service_provider" or "service_user"

    # Optional fields (for service providers)
    phone_number: Optional[str] = Field(default=None, alias="phoneNumber")
    service_type: Optional[List[str]] = Field(default=None, alias="serviceTypes")
    business_name: Optional[str] = Field(default=None, alias="businessName")
    address: Optional[str] = None
    latitude: Optional[float] = None  
    longitude: Optional[float] = None 
    available_hours: Optional[str] = Field(default=None, alias="availableHours")
    emergency_support: Optional[bool] = Field(default=False, alias="emergencySupport")
    hourly_rate: Optional[int] = Field(default=None, alias="hourlyRate")
    description: Optional[str] = Field(default="", alias="description")
    experience: Optional[str] = Field(default="", alias="experience")

    class Config:
        populate_by_name = True
        validate_by_name = True


# Schema for creating a new user
class FixNowUserCreate(FixNowUserBase):
    password: str = Field(..., min_length=8)


# Schema for returning user data (from DB)
class FixNowUser(FixNowUserBase):
    id: int
    keycloak_id: str

    class Config:
        from_attributes = True
        populate_by_name = True
        validate_by_name = True
