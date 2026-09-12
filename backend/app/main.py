import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, SessionLocal, engine
from . import models  # noqa: F401 — register models with metadata
from .routers import auth, consultation, diagnosis
from .seed import seed_demo_doctor, seed_diagnoses

app = FastAPI(title="ClinicCare Mini EMR", version="0.1.0")

allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://clinic-care-tau.vercel.app",
]
configured_origins = os.getenv("CLINICCARE_FRONTEND_URL", "")
allowed_origins.extend(
    origin.strip().strip('\"\'').rstrip("/")
    for origin in configured_origins.replace("\n", ",").split(",")
    if origin.strip().strip('\"\'')
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(diagnosis.router)
app.include_router(consultation.router)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_diagnoses(db)
        seed_demo_doctor(db)
    finally:
        db.close()


@app.get("/health")
def health():
    return {"status": "ok"}
