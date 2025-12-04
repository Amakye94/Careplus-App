# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date


# ==================== PATIENT =====================
class PatientCreate(BaseModel):
    name: str
    diabetes_type: str = "T2D"
    date_of_birth: Optional[date] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    weight: Optional[float] = None

    target: Optional[dict] = None
    emergency: Optional[dict] = None


class PatientOut(PatientCreate):
    id: int

    class Config:
        orm_mode = True


# ==================== READINGS =====================
class ReadingCreate(BaseModel):
    patient_id: int
    value_mgdl: float
    context: str = "random"
    notes: Optional[str] = None


class ReadingOut(BaseModel):
    id: int
    timestamp: datetime
    value_mgdl: float
    context: str
    notes: Optional[str]

    class Config:
        orm_mode = True


# ==================== ALERTS =====================
class AlertOut(BaseModel):
    id: int
    timestamp: datetime
    severity: str
    type: str
    message: str

    class Config:
        orm_mode = True


# ==================== HEART RATE =====================
class HeartRateCreate(BaseModel):
    bpm: int


class HeartRateOut(BaseModel):
    id: int
    bpm: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ==================== BLOOD PRESSURE =====================
class BloodPressureCreate(BaseModel):
    systolic: int
    diastolic: int


class BloodPressureOut(BaseModel):
    id: int
    systolic: int
    diastolic: int
    timestamp: datetime

    class Config:
        orm_mode = True


# ==================== MEDICATION =====================
class MedicationCreate(BaseModel):
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None


class MedicationOut(BaseModel):
    id: int
    name: str
    dosage: Optional[str]
    frequency: Optional[str]
    timestamp: Optional[datetime] = None

    class Config:
        orm_mode = True
