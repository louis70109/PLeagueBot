import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

db = SQLAlchemy()


engine = create_engine(os.getenv('DATABASE_URI'))
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

Base = declarative_base()

# Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
