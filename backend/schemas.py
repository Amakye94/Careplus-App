# backend/schemas.py
from __future__ import annotations
from datetime import datetime, date
from typing import Dict, Literal, Optional, List
from pydantic import BaseModel, Field, ConfigDict



# ==========================================================
#                     MEDICATIONS
# ==========================================================
class MedicationCreate(BaseModel):
    """Used for adding or updating a medication."""
    name: str
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    next_refill: Optional[date] = None
    notes: Optional[str] = None


class MedicationOut(MedicationCreate):
    """Returned when reading medication data."""
    id: int
    patient_id: int

    class Config:
        from_attributes = True


# ==========================================================
#                     READINGS
# ==========================================================
ReadingContext = Literal['fasting', 'pre_meal', 'post_meal', 'random']

class ReadingCreate(BaseModel):
    """Used for adding glucose readings."""
    patient_id: int
    value_mgdl: float = Field(ge=30, le=600)
    context: ReadingContext = 'random'
    notes: Optional[str] = None


class ReadingOut(BaseModel):
    """Returned when fetching glucose readings."""
    id: int
    patient_id: int
    timestamp: datetime
    value_mgdl: float
    context: ReadingContext
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
#                     ALERTS
# ==========================================================
class AlertOut(BaseModel):
    """Returned when listing alerts."""
    id: int
    patient_id: int
    timestamp: datetime
    severity: Literal['low', 'medium', 'high']
    type: str
    message: str

    model_config = ConfigDict(from_attributes=True)


# ==========================================================
#                     TARGET RANGES
# ==========================================================
class TargetRange(BaseModel):
    min: float
    max: float

class Targets(BaseModel):
    fasting: TargetRange
    post_meal: TargetRange
    random: TargetRange


# ==========================================================
#                     PATIENTS
# ==========================================================
class PatientCreate(BaseModel):
    """Used for creating or updating patients."""
    name: str
    diabetes_type: Literal['T1D', 'T2D'] = 'T2D'
    date_of_birth: Optional[date] = None
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    weight: Optional[float] = None
    target: Optional[Targets] = None
    emergency: Optional[Dict] = None


class PatientOut(BaseModel):
    """Returned when retrieving patient data."""
    id: int
    name: str
    diabetes_type: str
    date_of_birth: Optional[date]
    blood_pressure: Optional[str]
    heart_rate: Optional[int]
    weight: Optional[float]
    target: Optional[Targets] = None
    emergency: Optional[Dict] = None

    # Allow ORM mapping for SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)
