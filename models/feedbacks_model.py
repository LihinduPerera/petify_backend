from pydantic import BaseModel
from datetime import datetime

class FeedbackBase(BaseModel):
    user: str
    feedback: str
    time: datetime

class CreateFeedback(FeedbackBase):
    pass

class UpdateFeedback(FeedbackBase):
    pass 

class FeedbackResponse(FeedbackBase):
    id: str

    class Config:
        orm_mode = True