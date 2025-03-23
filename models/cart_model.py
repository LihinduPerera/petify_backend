from pydantic import BaseModel

class CartModel(BaseModel):
    user_id: str
    product_id: str
    quantity: int