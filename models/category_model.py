from pydantic import BaseModel

class CategoryBase(BaseModel):
    name: str
    image: str
    priority: int

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: str

    class Config:
        orm_mode = True