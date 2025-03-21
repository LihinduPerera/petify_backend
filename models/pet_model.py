from pydantic import BaseModel
from datetime import datetime
from typing import List , Optional

class PetBase(BaseModel):
    owner: str
    name: str
    species: str
    breed: str
    age: int
    gender: str
    dob : datetime
    medical_history: Optional[List[str]] = []

class PetCreate(PetBase):
    pass

class PetUpdate(PetBase):
    pass

class PetResponse(PetBase):
    id: str

    class Config:
        orm_mode = True