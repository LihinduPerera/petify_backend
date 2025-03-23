from fastapi import APIRouter , HTTPException
from models.cart_model import CartModel
from config.database import cart_collection
from bson import ObjectId

router = APIRouter()

def get_cart_collection(user_id: str):
    return cart_collection

@router.get("/{user_id}/cart")
async def read_user_cart(user_id: str):
    cart_items = list(get_cart_collection(user_id).find({"user_id": user_id}))
    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    for item in cart_items:
        item["_id"] = str(item["_id"])

    return cart_items

    
@router.post("/{user_id}/cart")
async def add_to_cart(user_id: str, cart_data: CartModel):
    cart_data.user_id = user_id

    cart_item = get_cart_collection(user_id).find_one({"user_id": user_id, "product_id": cart_data.product_id})

    if cart_item:
        get_cart_collection(user_id).update_one(
            {"user_id": user_id, "product_id": cart_data.product_id},
            {"$inc": {"quantity": 1}}
        )
    else:
        get_cart_collection(user_id).insert_one(cart_data.dict())

    return {"message": "Item added to cart"}


@router.delete("/{user_id}/cart/{product_id}")
async def delete_item_from_cart(user_id: str, product_id: str):
    result = get_cart_collection(user_id).delete_one({"product_id": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404,detail="Item not found")
    return {"message": "Item removed from cart"}

@router.delete("/{user_id}/cart")
async def empty_cart(user_id: str):
    result = get_cart_collection(user_id).delete_many({"user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Cart is already empty or user not found")
    return {"message": "Cart emptied successfully"}


@router.patch("/{user_id}/cart/{product_id}/decrease")
async def decrease_quantity(user_id: str, product_id: str):
    cart_item = get_cart_collection(user_id).find_one({"user_id": user_id, "product_id": product_id})
    if not cart_item:
        raise HTTPException(status_code=404, detail="Item not found in cart")

    if cart_item['quantity'] > 1:
        get_cart_collection(user_id).update_one(
            {"user_id": user_id, "product_id": product_id},
            {"$inc": {"quantity": -1}}
        )
        return {"message": "Quantity decreased"}
    else:
        get_cart_collection(user_id).delete_one({"user_id": user_id, "product_id": product_id})
        return {"message": "Item removed from cart"}
