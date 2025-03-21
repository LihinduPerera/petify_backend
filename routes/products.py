from fastapi import APIRouter, HTTPException , Query
from models.products_model import ProductCreate, ProductUpdate, ProductResponse
from config.database import product_collection
from bson import ObjectId

router = APIRouter()

def str_id(id: ObjectId) -> str:
    return str(id)

@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = product_collection.insert_one(product_dict)
    product_dict["id"] = str_id(result.inserted_id)
    return product_dict

@router.get("/products/", response_model=list[ProductResponse])
async def get_products():
    products = []
    for product in product_collection.find():
        product["id"] = str_id(product["_id"])
        products.append(product)
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product["id"] = str_id(product["_id"])
    return product

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):
    update_data = {key: value for key, value in product.dict().items() if value is not None}
    result = product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    updated_product = product_collection.find_one({"_id": ObjectId(product_id)})
    updated_product["id"] = str_id(updated_product["_id"])
    return updated_product

@router.delete("/products/{product_id}")
async def delete_product(product_id: str):
    result = product_collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

@router.get("/products/search/", response_model=list[ProductResponse])
async def search_products_by_name(query: str = Query(..., min_length=1, max_length=100)):
    products = []
    for product in product_collection.find({"name": {"$regex": query, "$options": "i"}}):
        product["id"] = str_id(product["_id"])
        products.append(product)
    return products

@router.put("/products/{product_id}/reduce_quantity/")
async def reduce_quantity(product_id: str, quantity: int):
    if quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
    product = product_collection.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    new_quantity = product['quantity'] - quantity
    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    product_collection.update_one({"_id": ObjectId(product_id)}, {"$set": {"quantity": new_quantity}})
    return {"message": f"Quantity reduced by {quantity}. New quantity: {new_quantity}"}
