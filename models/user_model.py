from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    address: str = None
    phone: str = None

class UserIn(BaseModel):
    name: str
    email: str
    password: str
    address: Optional[str] = None
    phone: Optional[str] = None

class UserOut(BaseModel):
    name: str
    email: str
    address: Optional[str] = None
    phone: Optional[str] = None

class UserUpdate(BaseModel):
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None

class ReadUsers(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class AdminLogin(BaseModel):
    email: str
    password: str