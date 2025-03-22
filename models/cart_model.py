from pydantic import BaseModel

class CartModel(BaseModel):
    product_id: str
    quantity: int