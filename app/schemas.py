from pydantic import BaseModel, Field, EmailStr

class ServiceProviderBase(BaseModel):
    full_name: str = Field(alias="fullName")
    phone_number: str = Field(alias="phoneNumber")
    email: EmailStr
    password: str = Field(..., min_length=8) 
    service_type: str = Field(alias="serviceType")
    business_name: str = Field(default="", alias="businessName")
    address: str
    available_hours: str = Field(alias="availableHours")
    emergency_support: bool = Field(default=False, alias="emergencySupport")
    hourly_rate: int = Field(alias="hourlyRate")
    description: str = Field(default="")
    experience: str = Field(default="")

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProvider(ServiceProviderBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2 compatibility
        populate_by_name = True
        allow_population_by_field_name = True
