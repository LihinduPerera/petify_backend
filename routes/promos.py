from fastapi import APIRouter , HTTPException
from models.promo_model import PromoResponse , PromoCreate , PromoUpdate
from config.database import promo_collection
from bson import ObjectId

router = APIRouter()

def str_id(id: ObjectId) -> str:
    return str(id)

@router.post("/promos/", response_model=PromoResponse)
async def create_promo(promo: PromoCreate):
    promo_dict = promo.dict()
    result = promo_collection.insert_one(promo_dict)
    promo_dict["id"] = str_id(result.inserted_id)
    return promo_dict

@router.get("/promos/",response_model=list[PromoResponse])
async def get_promos():
    promos = []
    for promo in promo_collection.find():
        promo["id"] = str_id(promo["_id"])
        promos.append(promo)
    return promos

@router.put("/promos/{promo_id}", response_model=PromoResponse)
async def update_promo(promo_id: str, promo: PromoUpdate):
    update_data = {key: value for key, value in promo.dict().items() if value is not None}
    result = promo_collection.update_one({"_id": ObjectId(promo_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Promo not found")
    update_promo = promo_collection.find_one({"_id": ObjectId(promo_id)})
    update_promo["id"] = str_id(update_promo["_id"])
    return update_promo

@router.delete("/promos/{promo_id}")
async def delete_promo(promo_id: str):
    result = promo_collection.delete_one({"_id": ObjectId(promo_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Promo not found")
    return {"detail": "Promo deleted successfully"}