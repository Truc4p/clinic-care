from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship

from .database import Base

consultation_diagnoses = Table(
    "consultation_diagnoses",
    Base.metadata,
    Column("consultation_id", Integer, ForeignKey("consultations.id"), primary_key=True),
    Column("diagnosis_code", String(16), ForeignKey("diagnoses.code"), primary_key=True),
)


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)

    consultations = relationship("Consultation", back_populates="doctor")


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    code = Column(String(16), primary_key=True)
    description = Column(String(512), nullable=False)

    consultations = relationship(
        "Consultation",
        secondary=consultation_diagnoses,
        back_populates="diagnoses",
    )


class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(255), nullable=False, index=True)
    notes = Column(Text, nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    doctor = relationship("Doctor", back_populates="consultations")
    diagnoses = relationship(
        "Diagnosis",
        secondary=consultation_diagnoses,
        back_populates="consultations",
    )
