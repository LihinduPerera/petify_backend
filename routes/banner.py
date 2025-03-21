from fastapi import APIRouter , HTTPException
from models.banner_model import BannerResponse , BannerCreate , BannerUpdate
from config.database import banner_collection
from bson import ObjectId

router = APIRouter()

def str_id(id: ObjectId) -> str:
    return str(id)

@router.post("/banners/" , response_model=BannerResponse)
async def create_banner(banner: BannerCreate):
    banner_dict = banner.dict()
    result = banner_collection.insert_one(banner_dict)
    banner_dict["id"] = str_id(result.inserted_id)
    return banner_dict

@router.get("/banners/", response_model=BannerResponse)
async def get_banners():
    banners = []
    for banner in banner_collection.find():
        banner["id"] = str_id(banner["id"])
        banners.append(banner)
    return banners

@router.put("/banners/{banner_id}", response_model=BannerResponse)
async def update_banner(banner_id: str, banner: BannerUpdate):
    update_data = {key: value for key, value in banner.dict().items() if value is not None}
    result = banner_collection.update_one({"id":ObjectId(banner_id)} , {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Banner not found")
    update_banner = banner_collection.find_one({"_id": ObjectId(banner_id)})
    update_banner["id"] = str_id(update_banner["_id"])
    return update_banner

@router.delete("/banners/{banner_id}", response_model=BannerResponse)
async def delete_banner(banner_id: str):
    result = banner_collection.delete_one({"_id": ObjectId(banner_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Banner not found")
    return {"detail": "Banner deleted successfully"}