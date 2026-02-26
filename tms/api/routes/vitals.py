from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List
import pandas as pd

router = APIRouter(prefix="/vitals", tags=["Health Monitoring"])

class VitalReading(BaseModel):
    heart_rate: int
    blood_sugar: float
    timestamp: datetime
    device_id: str

class HealthAlert(BaseModel):
    type: str  # fall|cardiac|glucose
    timestamp: datetime
    severity: str
    resolved: bool = False

vitals_data = pd.DataFrame(columns=['timestamp', 'heart_rate', 'blood_sugar', 'device_id'])
alerts_db = []

@router.post("/upload")
async def upload_vitals(reading: VitalReading):
    global vitals_data
    new_row = {
        'timestamp': reading.timestamp,
        'heart_rate': reading.heart_rate,
        'blood_sugar': reading.blood_sugar,
        'device_id': reading.device_id
    }
    vitals_data = vitals_data.append(new_row, ignore_index=True)
    
    # Simple anomaly detection
    if reading.heart_rate > 120 or reading.blood_sugar > 180:
        alert = HealthAlert(
            type="cardiac" if reading.heart_rate > 120 else "glucose",
            timestamp=datetime.now(),
            severity="high"
        )
        alerts_db.append(alert)
    
    return {"status": "received", "data_points": len(vitals_data)}

@router.get("/alerts", response_model=List[HealthAlert])
async def get_active_alerts():
    return [alert for alert in alerts_db if not alert.resolved]