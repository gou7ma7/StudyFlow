from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app.api import deps
from app.models.study import StudyRecord as StudyRecordModel
from app.schemas.study import StudyRecord, StudyRecordCreate

router = APIRouter(prefix="/study", tags=["study"])

@router.get("/", response_model=List[StudyRecord])
def get_study_records(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 10
):
    """获取学习记录列表"""
    records = db.query(StudyRecordModel).offset(skip).limit(limit).all()
    return records

@router.post("/", response_model=StudyRecord)
def create_study_record(
    record: StudyRecordCreate,
    db: Session = Depends(deps.get_db)
):
    """创建新的学习记录"""
    db_record = StudyRecordModel(
        title=record.title,
        duration=record.duration,
        date=record.date,
        notes=record.notes
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

@router.get("/{record_id}", response_model=StudyRecord)
def get_study_record(record_id: int, db: Session = Depends(deps.get_db)):
    """获取单个学习记录"""
    record = db.query(StudyRecordModel).filter(StudyRecordModel.id == record_id).first()
    if record is None:
        raise HTTPException(status_code=404, detail="Study record not found")
    return record 