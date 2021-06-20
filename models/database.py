import os
from databases import Database
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URI = os.getenv('DATABASE_URI')
engine = create_engine(URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
database = Database(URI)
Base = declarative_base()
