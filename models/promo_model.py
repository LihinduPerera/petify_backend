from pydantic import BaseModel

class PromoBase(BaseModel):
    category: str
    title: str
    image: str

class PromoCreate(PromoBase):
    pass

class PromoUpdate(PromoBase):
    pass

class PromoResponse(PromoBase):
    id: str

    class Config:
        orm_mode = True