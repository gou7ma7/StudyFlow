from app.db.base import Base, engine
from app.models.blog import BlogPost
from app.models.study import StudyRecord

def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()