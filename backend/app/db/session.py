from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker
from sqlalchemy.orm import declarative_base
from config.config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    print(settings.SQLALCHEMY_DATABASE_URI, flush=True)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

