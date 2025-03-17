from pydantic import BaseModel

class UserIn(BaseModel):
    name: str
    email: str
    password: str
    address: str = None
    phone: str = None

class UserOut(BaseModel):
    name: str
    email: str
    address: str = None
    phone: str = None