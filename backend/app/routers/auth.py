from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..auth import create_access_token, verify_password, get_current_doctor
from ..database import get_db
from ..models import Doctor
from ..schemas import LoginRequest, TokenResponse, DoctorOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.email == payload.email.lower()).first()
    if doctor is None or not verify_password(payload.password, doctor.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=doctor.email)
    return TokenResponse(access_token=token)


@router.get("/me", response_model=DoctorOut)
def me(current: Doctor = Depends(get_current_doctor)):
    """Return the currently-authenticated doctor profile."""
    return current
