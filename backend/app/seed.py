from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import hash_password
from .models import Diagnosis, Doctor

SEED_PATH = Path(__file__).resolve().parent.parent / "sql" / "seed_icd10.sql"

DEMO_DOCTOR_EMAIL = "doctor@clinic.care"
DEMO_DOCTOR_PASSWORD = "password123"
DEMO_DOCTOR_NAME = "Dr. Demo"


def seed_diagnoses(db: Session) -> int:
    """Load ICD-10 codes from SQL seed file if the diagnoses table is empty."""
    if db.query(Diagnosis).count() > 0:
        return 0

    sql = SEED_PATH.read_text(encoding="utf-8")
    if db.bind.dialect.name == "postgresql":
        sql = sql.replace(
            "INSERT OR IGNORE INTO diagnoses",
            "INSERT INTO diagnoses",
            1,
        ).rstrip().removesuffix(";") + " ON CONFLICT (code) DO NOTHING;"
    db.execute(text(sql))
    db.commit()
    return db.query(Diagnosis).count()


def seed_demo_doctor(db: Session) -> None:
    """Create the demo doctor account if it does not exist."""
    existing = db.query(Doctor).filter(Doctor.email == DEMO_DOCTOR_EMAIL).first()
    if existing:
        return
    doctor = Doctor(
        email=DEMO_DOCTOR_EMAIL.lower(),
        hashed_password=hash_password(DEMO_DOCTOR_PASSWORD),
        full_name=DEMO_DOCTOR_NAME,
    )
    db.add(doctor)
    db.commit()
