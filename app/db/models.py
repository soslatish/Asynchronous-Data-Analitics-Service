from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.db.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    
    devices = relationship("Device", back_populates="user")

class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    
    user = relationship("User", back_populates="devices")
    data = relationship("DeviceData", back_populates="device")

class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(String, primary_key=True, default=generate_uuid)
    device_id = Column(String, ForeignKey("devices.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    
    device = relationship("Device", back_populates="data")