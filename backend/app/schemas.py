from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class DiagnosisOut(BaseModel):
    code: str
    description: str

    model_config = {"from_attributes": True}


class DoctorOut(BaseModel):
    id: int
    email: str
    full_name: str

    model_config = {"from_attributes": True}


class ConsultationCreate(BaseModel):
    patient_name: str = Field(..., min_length=1, max_length=255)
    notes: str = Field(..., min_length=1)
    diagnosis_codes: list[str] = Field(default_factory=list)


class ConsultationOut(BaseModel):
    id: int
    patient_name: str
    notes: str
    created_at: datetime
    doctor: DoctorOut
    diagnoses: list[DiagnosisOut]

    model_config = {"from_attributes": True}


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
