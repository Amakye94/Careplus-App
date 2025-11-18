# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base



# ==========================================================
#                     PATIENT
# ==========================================================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    diabetes_type = Column(String, default="T2D")

    # Extended caregiver fields
    date_of_birth = Column(Date, nullable=True)
    blood_pressure = Column(String, nullable=True)   # e.g. "120/80 mmHg"
    heart_rate = Column(Integer, nullable=True)      # beats per minute
    weight = Column(Float, nullable=True)            # in kg

    # Existing optional target/emergency settings
    target = Column(JSON, default={
        "fasting": {"min": 80, "max": 130},
        "post_meal": {"min": 80, "max": 180},
        "random": {"min": 80, "max": 180}
    })
    emergency = Column(JSON, default=None)

    # Relationships
    readings = relationship("Reading", back_populates="patient", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")


# ==========================================================
#                     MEDICATION
# ==========================================================
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    name = Column(String, nullable=False)
    dosage = Column(String, nullable=True)
    frequency = Column(String, nullable=True)
    next_refill = Column(Date, nullable=True)
    notes = Column(String, nullable=True)

    # Relationship back to patient
    patient = relationship("Patient", back_populates="medications")


# ==========================================================
#                     READING
# ==========================================================
class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value_mgdl = Column(Float)
    context = Column(String, default="random")  # fasting | pre_meal | post_meal | random
    notes = Column(String, nullable=True)

    patient = relationship("Patient", back_populates="readings")


# ==========================================================
#                     ALERT
# ==========================================================
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(String)  # low | medium | high
    type = Column(String)
    message = Column(String)

    patient = relationship("Patient", back_populates="alerts")
