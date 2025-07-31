from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import models, database, schemas, crud

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/",)
def read_root():
    return {"message": "Welcome to fixNow backEnd"}

@app.post("/providers/", response_model=schemas.ServiceProvider)
def register_provider(provider: schemas.ServiceProviderCreate, db: Session = Depends(get_db)):
    return crud.create_service_provider(db, provider)

@app.get("/providers/", response_model=list[schemas.ServiceProvider])
def list_providers(db: Session = Depends(get_db)):
    return crud.get_service_providers(db)
