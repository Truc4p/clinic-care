from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from . import models  # noqa: F401 — register models with metadata
from .routers import consultation, diagnosis
from .seed import seed_diagnoses

app = FastAPI(title="ClinicCare Mini EMR", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(diagnosis.router)
app.include_router(consultation.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_diagnoses(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
