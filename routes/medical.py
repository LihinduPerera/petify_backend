from fastapi import APIRouter , HTTPException
from models.medical_model import MedicalResponse , MedicalCreate , MedicalUpdate
from config.database import medical_collection
from bson import ObjectId

router = APIRouter()

def str_id(id: ObjectId) -> str:
    return str(id)

@router.post("/medicals/", response_model=MedicalResponse)
async def create_medical(medical: MedicalCreate):
    medical_dict = medical.dict()
    result = medical_collection.insert_one(medical_dict)
    medical_dict["id"] = str_id(result.inserted_id)
    return medical_dict

@router.get("/medicals/",response_model=MedicalResponse)
async def get_medicals():
    medicals = []
    for medical in medical_collection.find():
        medical["id"] = str_id(medical["id"])
        medicals.append(medical)
    return medical

@router.put("/medicals/{medical_id}", response_model=MedicalResponse)
async def update_medical(medical_id:str, medical: MedicalUpdate):
    update_data = {key: value for key, value in medical.dict().items() if value is not None}
    result = medical_collection.update_one({"_id":ObjectId(medical_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Medical not found")
    update_medical = medical_collection.find_one({"_id": ObjectId(medical_id)})
    update_medical["id"] = str_id(update_medical["_id"])
    return update_medical

@router.delete("/medicals/{medical_id}", response_model=MedicalResponse)
async def delete_medical(medical_id: str):
    result = medical_collection.delete_one({"_id":ObjectId(medical_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Medical not found")
    return {"detail": "Medical deleted successfully"}