from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Diagnosis
from ..schemas import DiagnosisOut

router = APIRouter(tags=["diagnosis"])


@router.get("/diagnosis", response_model=list[DiagnosisOut])
def search_diagnosis(
    search: str | None = Query(default=None, description="Search term for code or description"),
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
):
    query = db.query(Diagnosis)
    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            or_(
                Diagnosis.code.ilike(term),
                Diagnosis.description.ilike(term),
            )
        )
    results = query.order_by(Diagnosis.code).limit(limit).all()
    return results
