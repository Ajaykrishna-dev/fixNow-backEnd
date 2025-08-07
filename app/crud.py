from sqlalchemy.orm import Session
from . import models, schemas

def create_service_provider(db: Session, provider: schemas.ServiceProviderCreate):
    # Convert the Pydantic model to dict and map to database field names
    provider_data = provider.model_dump(by_alias=False)  # Use snake_case field names
    db_provider = models.ServiceProvider(**provider_data)
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def get_service_providers(db: Session):
    return db.query(models.ServiceProvider).all()
