# backend/seed.py
from datetime import date, datetime, timedelta

from backend.db import SessionLocal, engine, Base
from backend import models

def run():
    print("🌱 Seeding Care+ database...")

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(models.Alert).delete()
    db.query(models.Reading).delete()
    db.query(models.Patient).delete()
    db.commit()

    # --- Create demo patients ---
    patients = [
        models.Patient(
            name="Ama Mensah",
            diabetes_type="T2D",
            date_of_birth=date(1984, 5, 22),
            blood_pressure="120/80 mmHg",
            heart_rate=72,
            weight=68.5
        ),
        models.Patient(
            name="Kwame Asare",
            diabetes_type="T1D",
            date_of_birth=date(1992, 8, 14),
            blood_pressure="130/85 mmHg",
            heart_rate=78,
            weight=73.2
        ),
        models.Patient(
            name="Akua Baah",
            diabetes_type="T2D",
            date_of_birth=date(1975, 12, 3),
            blood_pressure="118/79 mmHg",
            heart_rate=70,
            weight=65.0
        )
    ]

    db.add_all(patients)
    db.commit()

    # --- Create some glucose readings for each patient ---
    for p in patients:
        readings = []
        base_time = datetime.utcnow() - timedelta(days=7)
        for i in range(7):  # one reading per day
            readings.append(models.Reading(
                patient_id=p.id,
                timestamp=base_time + timedelta(days=i),
                value_mgdl=90 + i * 5,  # fake pattern
                context="random",
                notes="Auto-generated sample"
            ))
        db.add_all(readings)
    db.commit()

    # --- Create example alerts ---
    alerts = [
        models.Alert(
            patient_id=patients[0].id,
            severity="medium",
            type="glucose",
            message="Glucose slightly above target range."
        ),
        models.Alert(
            patient_id=patients[1].id,
            severity="high",
            type="blood_pressure",
            message="Blood pressure higher than normal."
        ),
    ]

    db.add_all(alerts)
    db.commit()
    db.close()

    print("✅ Seeding complete! Added demo patients, readings, and alerts.")


if __name__ == "__main__":
    run()
