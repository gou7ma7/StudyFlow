from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional

class StudyRecordBase(BaseModel):
    title: str
    duration: timedelta
    date: datetime
    notes: Optional[str] = None

class StudyRecordCreate(StudyRecordBase):
    pass

class StudyRecord(StudyRecordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 