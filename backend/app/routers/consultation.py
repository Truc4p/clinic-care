from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload

from ..auth import get_current_doctor
from ..database import get_db
from ..models import Consultation, Diagnosis, Doctor
from ..schemas import ConsultationCreate, ConsultationOut

router = APIRouter(tags=["consultation"])


@router.post(
    "/consultation",
    response_model=ConsultationOut,
    status_code=status.HTTP_201_CREATED,
)
def create_consultation(
    payload: ConsultationCreate,
    db: Session = Depends(get_db),
    doctor: Doctor = Depends(get_current_doctor),
):
    codes = [c.strip() for c in payload.diagnosis_codes if c and c.strip()]
    if not codes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one diagnosis code is required.",
        )

    unique_codes = list(dict.fromkeys(codes))
    diagnoses = db.query(Diagnosis).filter(Diagnosis.code.in_(unique_codes)).all()
    found_codes = {d.code for d in diagnoses}
    missing = [c for c in unique_codes if c not in found_codes]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown diagnosis code(s): {', '.join(missing)}",
        )

    consultation = Consultation(
        patient_name=payload.patient_name.strip(),
        notes=payload.notes.strip(),
        doctor_id=doctor.id,
        diagnoses=diagnoses,
    )
    db.add(consultation)
    db.commit()

    return (
        db.query(Consultation)
        .options(joinedload(Consultation.doctor), joinedload(Consultation.diagnoses))
        .filter(Consultation.id == consultation.id)
        .one()
    )


@router.get("/consultation", response_model=list[ConsultationOut])
def list_consultations(
    patient: str | None = Query(default=None, description="Filter by patient name"),
    diagnosis: str | None = Query(
        default=None, description="Filter by diagnosis code or description"
    ),
    db: Session = Depends(get_db),
    _: Doctor = Depends(get_current_doctor),
):
    query = db.query(Consultation).options(
        joinedload(Consultation.doctor),
        joinedload(Consultation.diagnoses),
    )

    if patient and patient.strip():
        query = query.filter(Consultation.patient_name.ilike(f"%{patient.strip()}%"))

    if diagnosis and diagnosis.strip():
        term = f"%{diagnosis.strip()}%"
        query = (
            query.join(Consultation.diagnoses)
            .filter((Diagnosis.code.ilike(term)) | (Diagnosis.description.ilike(term)))
            .distinct()
        )

    return query.order_by(Consultation.created_at.desc()).all()
