from fastapi import APIRouter, HTTPException
from config.database import pet_collection
from models.pet_model import PetCreate , PetUpdate
from bson import ObjectId

router = APIRouter()

def get_pet_collection(user_id: str):
    return pet_collection

def str_id(id: ObjectId) -> str:
    return str(id)

@router.get("/{user_id}/pets")
async def read_user_pets(user_id: str):
    pets = list(get_pet_collection(user_id).find({"owner": user_id}))
    if not pets:
        raise HTTPException(status_code=404, detail="Pets not found")
    for pet in pets:
        pet["_id"] = str(pet["_id"])

    return pets

@router.post("/{user_id}/pets")
async def add_pet(user_id: str, pet_data: PetCreate):   
    pet_data.owner = user_id
    pet_dict = pet_data.dict()
    result = get_pet_collection(user_id).insert_one(pet_dict)
    pet_dict["id"] = str_id(result.inserted_id)
    return pet_dict

@router.put("/pets/{pet_id}")
async def update_pet(pet_id: str, pet_data: PetUpdate):
    pet = get_pet_collection().find_one({"_id": ObjectId(pet_id)})
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")

    updated_data = pet_data.dict(exclude_unset=True)
    result = get_pet_collection().update_one(
        {"_id": ObjectId(pet_id)}, 
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    updated_pet = get_pet_collection().find_one({"_id": ObjectId(pet_id)})
    updated_pet["_id"] = str(updated_pet["_id"])
    return updated_pet

@router.delete("/pets/{pet_id}")
async def delete_pet(pet_id: str):

    pet = get_pet_collection().find_one({"_id": ObjectId(pet_id)})
    if not pet:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    result = get_pet_collection().delete_one({"_id": ObjectId(pet_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Pet not found")

    return {"message": "Pet deleted successfully"}