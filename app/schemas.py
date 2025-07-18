from pydantic import BaseModel

class ServiceProviderBase(BaseModel):
    full_name: str
    phone_number: str
    service_type: str
    business_name: str = ""
    address: str
    available_hours: str
    emergency_support: bool = False
    hourly_rate: int
    description: str = ""
    experience: str = ""

class ServiceProviderCreate(ServiceProviderBase):
    pass

class ServiceProvider(ServiceProviderBase):
    id: int

    class Config:
        from_attributes = True  # for Pydantic v2 compatibility
