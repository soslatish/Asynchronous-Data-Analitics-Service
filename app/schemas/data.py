from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime

class DeviceDataCreate(BaseModel):
    x: float
    y: float
    z: float

class DeviceData(DeviceDataCreate):
    id: str
    device_id: str
    timestamp: datetime

    class Config:
        orm_mode = True

class AnalyticsResult(BaseModel):
    min: float
    max: float
    count: int
    sum: float
    median: float

class DeviceAnalytics(BaseModel):
    x: AnalyticsResult
    y: AnalyticsResult
    z: AnalyticsResult