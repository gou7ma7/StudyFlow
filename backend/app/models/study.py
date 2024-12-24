from sqlalchemy import Column, Integer, String, Text, DateTime, Interval
from sqlalchemy.sql import func
from app.db.base import Base

class StudyRecord(Base):
    __tablename__ = "study_records"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    duration = Column(Interval, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 