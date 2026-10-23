from fastapi import FastAPI
from app.database import Base, engine
from app import models  # noqa: F401  (registers the tables)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Retail Portal API")


@app.get("/")
def health():
    return {"status": "ok", "message": "Retail Portal API is running"}