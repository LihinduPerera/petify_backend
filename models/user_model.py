from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    address: str = None
    phone: str = None