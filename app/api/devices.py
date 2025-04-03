from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.db.models import Device, DeviceData
from app.schemas.device import DeviceCreate, Device as DeviceSchema
from app.schemas.data import DeviceDataCreate

router = APIRouter()

@router.post("/", response_model=DeviceSchema, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    db_device = Device(name=device.name, user_id=device.user_id)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.get("/{device_id}", response_model=DeviceSchema)
def get_device(device_id: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.post("/{device_id}/data", status_code=status.HTTP_201_CREATED)
def add_device_data(device_id: str, data: DeviceDataCreate, db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
 
        device = Device(id=device_id, name=f"Device {device_id}")
        db.add(device)
        db.commit()
        db.refresh(device)
    
    device_data = DeviceData(
        device_id=device_id,
        x=data.x,
        y=data.y,
        z=data.z
    )
    db.add(device_data)
    db.commit()
    return {"status": "success", "message": "Data added successfully"}