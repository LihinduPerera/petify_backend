from fastapi import APIRouter , HTTPException
from models.category_model import CategoryCreate , CategoryResponse , CategoryUpdate
from config.database import category_collection
from bson import ObjectId

router = APIRouter()

def str_id(id: ObjectId) -> str:
    return str(id)

@router.post("/categories/",response_model=CategoryResponse)
async def create_category(category: CategoryCreate):
    category_dict = category.dict()
    result = category_collection.insert_one(category_dict)
    category_dict["id"] = str_id(result.inserted_id)
    return category_dict

@router.get("/categories/",response_model=CategoryResponse)
async def get_categories():
    categories = []
    for category in category_collection.find():
        category["id"] = str_id(category["id"])
        categories.append(category)
    return categories

@router.put("/categories/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: str, category:CategoryUpdate):
    update_data = {key: value for key, value in category.dict().items() if value is not None}
    result = category_collection.update_one({"_id": ObjectId(category_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    update_category = category_collection.find_one({"_id": ObjectId(category_id)})
    update_category["id"] = str_id(update_category["_id"])
    return update_category

@router.delete("/categories/{category_id}", response_model=CategoryResponse)
async def delete_category(category_id: str):
    result = category_collection.delete_one({"_id": ObjectId(category_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"detail": "Category deleted successfully"}