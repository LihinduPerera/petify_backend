from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PetBase(BaseModel):
    owner: str
    name: Optional[str] = None
    species: Optional[str] = None
    breed: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class PetCreate(PetBase):
    pass

class PetUpdate(PetBase):
    pass

class PetResponse(PetBase):
    id: str

    class Config:
        orm_mode = True