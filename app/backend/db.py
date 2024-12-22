from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine('sqlite:///gamemanager.db')

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()