from fastapi import APIRouter, HTTPException
from config.database import medical_collection
from models.medical_model import MedicalCreate, MedicalUpdate
from bson import ObjectId
from datetime import datetime , date

router = APIRouter()

def get_medical_collection(pet_id: str):
    return medical_collection

def str_id(id: ObjectId) -> str:
    return str(id)

def convert_to_datetime(date: date) -> datetime:
    """Helper function to convert datetime.date to datetime.datetime"""
    return datetime(date.year, date.month, date.day)

@router.get("/{pet_id}/medicals")
async def read_pet_medicals(pet_id: str):
    medicals = list(get_medical_collection(pet_id).find({"pet": pet_id}))
    if not medicals:
        raise HTTPException(status_code=404, detail="Medicals not found")
    for medical in medicals:
        medical["_id"] = str(medical["_id"])
    return medicals

@router.post("/{pet_id}/medicals")
async def add_medical(pet_id: str, medical_data: MedicalCreate):
    medical_data.pet = pet_id
    medical_data.isNotified = False
    medical_data.isNewMedical = True
    medical_dict = medical_data.dict()
    
    if isinstance(medical_dict["date"], date):
        medical_dict["date"] = convert_to_datetime(medical_dict["date"])

    result = get_medical_collection(pet_id).insert_one(medical_dict)
    medical_dict["_id"] = str_id(result.inserted_id)
    return medical_dict

@router.put("/medicals/{medical_id}")
async def update_medical(medical_id: str, medical_data: MedicalUpdate):
    medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    if not medical:
        raise HTTPException(status_code=404, detail="Medical is not found")
    
    updated_data = {
        "date": medical_data.date,
        "medication": medical_data.medication,
        "notes": medical_data.notes,
        "status": medical_data.status
    }
    
    if isinstance(updated_data.get("date"), date):
        updated_data["date"] = convert_to_datetime(updated_data["date"])

    result = medical_collection.update_one(
        {"_id": ObjectId(medical_id)}, 
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Medical is not found")
    
    updated_medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    updated_medical["_id"] = str(updated_medical["_id"])
    return updated_medical


@router.delete("/medicals/{medical_id}")
async def delete_medical(medical_id: str):
    medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    if not medical:
        raise HTTPException(status_code=404, detail="Medical is not found")
    
    result = medical_collection.delete_one({"_id": ObjectId(medical_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Medical is not found")
    
    return {"message": "Medical deleted successfully"}

@router.patch("/medicals/{medical_id}/notification")
async def update_notification_flags(medical_id: str, notification_data: dict):
    
    medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    if not medical:
        raise HTTPException(status_code=404, detail="Medical record not found.")
    
    updated_data = {}
    
    if "isNotified" in notification_data:
        updated_data["isNotified"] = notification_data["isNotified"]
    
    if "isNewMedical" in notification_data:
        updated_data["isNewMedical"] = notification_data["isNewMedical"]

    result = medical_collection.update_one(
        {"_id": ObjectId(medical_id)},
        {"$set": updated_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Medical record not found.")

    updated_medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    updated_medical["_id"] = str(updated_medical["_id"])
    
    return updated_medical

