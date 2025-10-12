from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .crud import crud
from .db import database
from .models import models
from .schemas import schemas

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict later to your frontend domain
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


@app.get("/")
def read_root():
    return {"message": "Welcome to fixNow backEnd"}


@app.get("/providers/", response_model=list[schemas.FixNowUser])
def list_providers(db: Session = Depends(get_db)):
    # Only service providers
    return crud.get_service_providers(db)


@app.post("/providers/", response_model=schemas.FixNowUser)
def register_provider(provider: schemas.FixNowUserCreate, db: Session = Depends(get_db)):
    return crud.create_user_with_role(provider, "service_providers", db)


@app.post("/users/", response_model=schemas.FixNowUser)
def register_user(user: schemas.FixNowUserCreate, db: Session = Depends(get_db)):
    return crud.create_user_with_role(user, "service_user", db)
