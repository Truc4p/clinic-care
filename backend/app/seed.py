from pathlib import Path

from sqlalchemy import text
from sqlalchemy.orm import Session

from ..models import Diagnosis

SEED_PATH = Path(__file__).resolve().parent.parent / "sql" / "seed_icd10.sql"


def seed_diagnoses(db: Session) -> int:
    """Load ICD-10 codes from SQL seed file if the diagnoses table is empty."""
    if db.query(Diagnosis).count() > 0:
        return 0

    sql = SEED_PATH.read_text(encoding="utf-8")
    db.execute(text(sql))
    db.commit()
    return db.query(Diagnosis).count()
