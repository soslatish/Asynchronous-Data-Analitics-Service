from pydantic import BaseModel, EmailStr
from typing import List, Optional
from app.schemas.device import Device

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: str
    devices: Optional[List[Device]] = []

    class Config:
        orm_mode = True