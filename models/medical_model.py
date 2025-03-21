from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MedicalBase(BaseModel):
    pet: str
    date: datetime
    medication: str
    notes: Optional[str] = None
    status: str

class MedicalCreate(MedicalBase):
    pass

class MedicalUpdate(MedicalBase):
    pass

class MedicalResponse(MedicalBase):
    id: str
    
    class Config: 
        orm_mode= True