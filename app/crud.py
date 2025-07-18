from sqlalchemy.orm import Session
from . import models, schemas

def create_service_provider(db: Session, provider: schemas.ServiceProviderCreate):
    db_provider = models.ServiceProvider(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider

def get_service_providers(db: Session):
    return db.query(models.ServiceProvider).all()
