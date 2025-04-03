from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
import statistics
from datetime import datetime, timedelta
from app.db.database import get_db
from app.db.models import Device, DeviceData, User
from app.schemas.data import DeviceAnalytics, AnalyticsResult
from app.tasks.analytics import process_analytics  

router = APIRouter()

def calculate_analytics(data_points, field):
    if not data_points:
        return AnalyticsResult(min=0, max=0, count=0, sum=0, median=0)
    
    values = [getattr(point, field) for point in data_points]
    return AnalyticsResult(
        min=min(values),
        max=max(values),
        count=len(values),
        sum=sum(values),
        median=statistics.median(values) if values else 0
    )

@router.get("/devices/{device_id}", response_model=DeviceAnalytics)
def get_device_analytics(
    device_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    query = db.query(DeviceData).filter(DeviceData.device_id == device_id)
    
    if start_time:
        query = query.filter(DeviceData.timestamp >= start_time)
    if end_time:
        query = query.filter(DeviceData.timestamp <= end_time)
    
    data_points = query.all()
    
    x_analytics = calculate_analytics(data_points, "x")
    y_analytics = calculate_analytics(data_points, "y")
    z_analytics = calculate_analytics(data_points, "z")
    
    return DeviceAnalytics(
        x=x_analytics,
        y=y_analytics,
        z=z_analytics
    )

@router.get("/users/{user_id}", response_model=Dict[str, DeviceAnalytics])
def get_user_analytics(
    user_id: str,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregate: bool = True,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    devices = db.query(Device).filter(Device.user_id == user_id).all()
    if not devices:
        return {"message": "No devices found for user"}
    
    result = {}
    
    if aggregate:
        device_ids = [device.id for device in devices]
        query = db.query(DeviceData).filter(DeviceData.device_id.in_(device_ids))
        
        if start_time:
            query = query.filter(DeviceData.timestamp >= start_time)
        if end_time:
            query = query.filter(DeviceData.timestamp <= end_time)
        
        data_points = query.all()
        
        x_analytics = calculate_analytics(data_points, "x")
        y_analytics = calculate_analytics(data_points, "y")
        z_analytics = calculate_analytics(data_points, "z")
        
        result["aggregated"] = DeviceAnalytics(
            x=x_analytics,
            y=y_analytics,
            z=z_analytics
        )
    else:
        for device in devices:
            result[device.id] = get_device_analytics(
                device_id=device.id,
                start_time=start_time,
                end_time=end_time,
                db=db
            )
    
    return result
