from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.database.config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Base model for SQLAlchemy ORM
Base = declarative_base()
