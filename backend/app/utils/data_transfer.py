import json
from datetime import datetime
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from app.db.base import SessionLocal
from app.models.blog import BlogPost
from app.models.study import StudyRecord

class DataTransfer:
    @staticmethod
    def export_data() -> Dict[str, List[Dict[str, Any]]]:
        """导出所有数据"""
        db = SessionLocal()
        try:
            blog_posts = db.query(BlogPost).all()
            study_records = db.query(StudyRecord).all()
            
            data = {
                "blog_posts": [
                    {
                        "id": post.id,
                        "title": post.title,
                        "content": post.content,
                        "created_at": post.created_at.isoformat(),
                        "updated_at": post.updated_at.isoformat() if post.updated_at else None
                    }
                    for post in blog_posts
                ],
                "study_records": [
                    {
                        "id": record.id,
                        "title": record.title,
                        "duration": str(record.duration),
                        "date": record.date.isoformat(),
                        "notes": record.notes
                    }
                    for record in study_records
                ]
            }
            return data
        finally:
            db.close()
    
    @staticmethod
    def import_data(data: Dict[str, List[Dict[str, Any]]]):
        """导入所有数据"""
        db = SessionLocal()
        try:
            for post_data in data.get("blog_posts", []):
                post = BlogPost(
                    title=post_data["title"],
                    content=post_data["content"],
                    created_at=datetime.fromisoformat(post_data["created_at"]),
                    updated_at=datetime.fromisoformat(post_data["updated_at"]) if post_data["updated_at"] else None
                )
                db.add(post)
            
            for record_data in data.get("study_records", []):
                record = StudyRecord(
                    title=record_data["title"],
                    duration=record_data["duration"],
                    date=datetime.fromisoformat(record_data["date"]),
                    notes=record_data["notes"]
                )
                db.add(record)
            
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

def export_to_file(filename: str = "backup.json"):
    """导出数据到文件"""
    data = DataTransfer.export_data()
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def import_from_file(filename: str = "backup.json"):
    """从文件导入数据"""
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    DataTransfer.import_data(data)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python data_transfer.py [export|import] [filename]")
        sys.exit(1)
    
    action = sys.argv[1]
    filename = sys.argv[2] if len(sys.argv) > 2 else "backup.json"
    
    if action == "export":
        export_to_file(filename)
        print(f"Data exported to {filename}")
    elif action == "import":
        import_from_file(filename)
        print(f"Data imported from {filename}") 