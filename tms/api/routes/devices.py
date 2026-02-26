from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/devices", tags=["Device Management"])

class Device(BaseModel):
    id: str
    type: str  # wearable|hub|sensor
    last_connected: datetime
    firmware_version: str
    status: str = "offline"

class DeviceRegistration(BaseModel):
    mac_address: str
    device_type: str
    initial_config: dict

devices_db = []

@router.post("/register", response_model=Device)
async def register_device(registration: DeviceRegistration):
    new_device = Device(
        id=registration.mac_address,
        type=registration.device_type,
        last_connected=datetime.now(),
        firmware_version="1.0.0",
        status="active"
    )
    devices_db.append(new_device)
    return new_device

@router.get("/", response_model=List[Device])
async def list_devices():
    return devices_db

@router.get("/{device_id}/status")
async def device_status(device_id: str):
    for device in devices_db:
        if device.id == device_id:
            return {
                "status": device.status,
                "last_connected": device.last_connected,
                "firmware": device.firmware_version
            }
    raise HTTPException(status_code=404, detail="Device not found")