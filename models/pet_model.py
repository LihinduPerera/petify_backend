from pydantic import BaseModel
from datetime import datetime

class PetBase(BaseModel):
    owner: str
    name: str
    species: str
    breed: str
    age: int
    gender: str
    dob : datetime

class PetCreate(PetBase):
    pass

class PetUpdate(PetBase):
    pass

class PetResponse(PetBase):
    id: str

    class Config:
        orm_mode = True