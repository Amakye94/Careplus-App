# backend/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


# ======================= PATIENT ==========================
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    diabetes_type = Column(String, default="T2D")

    date_of_birth = Column(Date, nullable=True)
    blood_pressure = Column(String, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)

    target = Column(JSON, default={
        "fasting": {"min": 80, "max": 130},
        "post_meal": {"min": 80, "max": 180},
        "random": {"min": 80, "max": 180}
    })
    emergency = Column(JSON, default=None)

    readings = relationship("Reading", back_populates="patient", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="patient", cascade="all, delete-orphan")
    medications = relationship("Medication", back_populates="patient", cascade="all, delete-orphan")
    heartrate = relationship("HeartRate", cascade="all, delete-orphan")
    bloodpressure = relationship("BloodPressure", cascade="all, delete-orphan")


# ======================= MEDICATION =======================
class Medication(Base):
    __tablename__ = "medications"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    name = Column(String, nullable=False)
    dosage = Column(String)
    frequency = Column(String)

    patient = relationship("Patient", back_populates="medications")


# ======================= READING ==========================
class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    value_mgdl = Column(Float)
    context = Column(String, default="random")
    notes = Column(String)

    patient = relationship("Patient", back_populates="readings")


# ======================= ALERT ============================
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    severity = Column(String)
    type = Column(String)
    message = Column(String)

    patient = relationship("Patient", back_populates="alerts")


# ======================= HEART RATE =======================
class HeartRate(Base):
    __tablename__ = "heartrate"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    bpm = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)


# ======================= BLOOD PRESSURE ===================
class BloodPressure(Base):
    __tablename__ = "bloodpressure"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    systolic = Column(Integer)
    diastolic = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
