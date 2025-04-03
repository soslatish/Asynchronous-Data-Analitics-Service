from celery import shared_task
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
import statistics
from datetime import datetime
from app.db.models import Device, DeviceData, User
from typing import List, Dict, Any, Optional

@shared_task
def process_analytics(
    device_id: str, 
    start_time: Optional[str] = None, 
    end_time: Optional[str] = None
) -> Dict[str, Any]:
    db = SessionLocal()
    try:
        query = db.query(DeviceData).filter(DeviceData.device_id == device_id)
        
        if start_time:
            start_datetime = datetime.fromisoformat(start_time)
            query = query.filter(DeviceData.timestamp >= start_datetime)
        if end_time:
            end_datetime = datetime.fromisoformat(end_time)
            query = query.filter(DeviceData.timestamp <= end_datetime)
        
        data_points = query.all()
        
        result = {}
        for field in ["x", "y", "z"]:
            if not data_points:
                result[field] = {
                    "min": 0, "max": 0, "count": 0, "sum": 0, "median": 0
                }
            else:
                values = [getattr(point, field) for point in data_points]
                result[field] = {
                    "min": min(values),
                    "max": max(values),
                    "count": len(values),
                    "sum": sum(values),
                    "median": statistics.median(values) if values else 0
                }
        
        return result
    finally:
        db.close()