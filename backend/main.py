# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session
from typing import List

from backend.db import Base, engine, get_db
from backend import models, schemas, rules

app = FastAPI(title="Care+ API", version="1.0")

# ---------------- CORS MIDDLEWARE ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- CREATE TABLES ------------------
Base.metadata.create_all(bind=engine)


# ---------------- HEALTH CHECK -------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------- PATIENT CRUD -------------------
@app.post("/patients", response_model=schemas.PatientOut)
def create_patient(payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    p = models.Patient(
        name=payload.name,
        diabetes_type=payload.diabetes_type,
        date_of_birth=payload.date_of_birth,
        blood_pressure=payload.blood_pressure,
        heart_rate=payload.heart_rate,
        weight=payload.weight,
        target=payload.target,
        emergency=payload.emergency,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p


@app.get("/patients", response_model=List[schemas.PatientOut])
def list_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).order_by(models.Patient.id.desc()).all()


@app.get("/patients/{patient_id}", response_model=schemas.PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Patient).get(patient_id)
    if not p:
        raise HTTPException(404, "Patient not found")
    return p


@app.put("/patients/{patient_id}", response_model=schemas.PatientOut)
def update_patient(patient_id: int, payload: schemas.PatientCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).get(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    for key, value in payload.dict().items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).get(patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    db.delete(patient)
    db.commit()
    return {"detail": "Patient deleted"}


# ---------------- READINGS -------------------
@app.post("/readings", response_model=schemas.ReadingOut)
def add_reading(payload: schemas.ReadingCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).get(payload.patient_id)
    if not patient:
        raise HTTPException(404, "Patient not found")

    r = models.Reading(
        patient_id=payload.patient_id,
        value_mgdl=payload.value_mgdl,
        context=payload.context,
        notes=payload.notes,
    )
    db.add(r)

    # Rule-based alert engine
    alerts_from_reading = rules.evaluate_reading(patient, r)
    for a in alerts_from_reading:
        db.add(a)

    db.commit()
    db.refresh(r)
    return r


@app.get("/patients/{patient_id}/readings", response_model=List[schemas.ReadingOut])
def list_readings(patient_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Reading)
        .filter(models.Reading.patient_id == patient_id)
        .order_by(models.Reading.timestamp.desc())
        .all()
    )


# ---------------- ALERTS -------------------
@app.get("/patients/{patient_id}/alerts", response_model=List[schemas.AlertOut])
def list_alerts(patient_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Alert)
        .filter(models.Alert.patient_id == patient_id)
        .order_by(models.Alert.timestamp.desc())
        .all()
    )


# ---------------- HEART RATE -------------------
@app.get("/patients/{patient_id}/heartrate", response_model=List[schemas.HeartRateOut])
def get_heart_rate(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.HeartRate).filter(models.HeartRate.patient_id == patient_id).all()


@app.post("/patients/{patient_id}/heartrate", response_model=schemas.HeartRateOut)
def add_heart_rate(patient_id: int, data: schemas.HeartRateCreate, db: Session = Depends(get_db)):
    hr = models.HeartRate(patient_id=patient_id, bpm=data.bpm)
    db.add(hr)
    db.commit()
    db.refresh(hr)
    return hr


# ---------------- BLOOD PRESSURE -------------------
@app.get("/patients/{patient_id}/bloodpressure", response_model=List[schemas.BloodPressureOut])
def get_blood_pressure(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.BloodPressure).filter(models.BloodPressure.patient_id == patient_id).all()


@app.post("/patients/{patient_id}/bloodpressure", response_model=schemas.BloodPressureOut)
def add_blood_pressure(patient_id: int, data: schemas.BloodPressureCreate, db: Session = Depends(get_db)):
    bp = models.BloodPressure(
        patient_id=patient_id,
        systolic=data.systolic,
        diastolic=data.diastolic
    )
    db.add(bp)
    db.commit()
    db.refresh(bp)
    return bp


# ---------------- MEDICATIONS -------------------
@app.get("/patients/{patient_id}/medications", response_model=List[schemas.MedicationOut])
def list_meds(patient_id: int, db: Session = Depends(get_db)):
    return db.query(models.Medication).filter(models.Medication.patient_id == patient_id).all()


@app.post("/patients/{patient_id}/medications", response_model=schemas.MedicationOut)
def add_med(patient_id: int, data: schemas.MedicationCreate, db: Session = Depends(get_db)):
    m = models.Medication(
        patient_id=patient_id,
        name=data.name,
        dosage=data.dosage,
        frequency=data.frequency
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@app.delete("/medications/{med_id}")
def delete_med(med_id: int, db: Session = Depends(get_db)):
    m = db.query(models.Medication).get(med_id)
    if not m:
        raise HTTPException(404, "Medication not found")

    db.delete(m)
    db.commit()
    return {"detail": "Medication deleted"}


# ---------------- ROOT ROUTES ----------------
@app.get("/", include_in_schema=False)
def root():
    return JSONResponse({"message": "Care+ API running."})


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return PlainTextResponse("", status_code=204)
