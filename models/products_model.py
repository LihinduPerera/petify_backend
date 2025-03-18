from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    desc: str
    image: str
    old_price: int
    new_price: int
    category: str
    quantity: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str

    class Config:
        orm_mode = True