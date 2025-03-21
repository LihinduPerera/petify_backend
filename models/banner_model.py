from pydantic import BaseModel

class BannerBase(BaseModel):
    category: str
    title: str
    image: str

class BannerCreate(BannerBase):
    pass

class BannerUpdate(BannerBase):
    pass

class BannerResponse(BannerBase):
    id: str

    class Config:
        orm_mode = True