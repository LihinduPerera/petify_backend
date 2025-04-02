from fastapi import APIRouter, HTTPException
from models.feedbacks_model import CreateFeedback
from config.database import feedback_collection
from bson import ObjectId

router = APIRouter()

def get_feedback_collection(user_id: str):
    return feedback_collection

def str_id(id: ObjectId) -> str:
    return str(id)

@router.get("/{user_id}/feedbacks")
async def read_feedbacks(user_id: str):
    feedbacks = list(get_feedback_collection(user_id).find({"user": user_id}))
    if not feedbacks:
        raise HTTPException(status_code=404, detail="Feedbacks not found")
    for feedback in feedbacks:
        feedback["_id"] = str(feedback["_id"])
    return feedbacks

@router.post("/{user_id}/feedbacks")
async def add_feedback(user_id: str, feedback_data: CreateFeedback):
    feedback_data.user = user_id
    feedback_dict = feedback_data.dict()
    result = get_feedback_collection(user_id).insert_one(feedback_dict)
    feedback_dict["_id"] = str_id(result.inserted_id)
    return feedback_dict

@router.delete("/feedbacks/{feedback_id}")
async def delete_feedback(feedback_id: str):

    feedback = feedback_collection.find_one({"_id": ObjectId(feedback_id)})
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    result = feedback_collection.delete_one({"_id": ObjectId(feedback_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    return {"message": "Feedback deleted successfully"}