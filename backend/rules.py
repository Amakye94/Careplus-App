from typing import List
from .models import Patient, Reading, Alert
from datetime import datetime

def evaluate_reading(patient: Patient, reading: Reading) -> List[Alert]:
    alerts: List[Alert] = []
    t = patient.target or {
        "fasting": {"min": 80, "max": 130},
        "post_meal": {"min": 80, "max": 180},
        "random": {"min": 80, "max": 180}
    }
    ctx = reading.context or 'random'
    target = t.get(ctx, t["random"])  # type: ignore
    low, high = target["min"], target["max"]

    if reading.value_mgdl < low or reading.value_mgdl > high:
        severe = reading.value_mgdl < 54 or reading.value_mgdl > 300
        alerts.append(
            Alert(
                patient_id=patient.id,
                timestamp=datetime.utcnow(),
                severity='high' if severe else 'medium',
                type='reading_range',
                message=(
                    f"Dangerous glucose {reading.value_mgdl} mg/dL" if severe
                    else f"Out-of-range glucose {reading.value_mgdl} mg/dL"
                )
            )
        )
    return alerts
