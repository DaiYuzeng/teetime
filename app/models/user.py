from sqlalchemy import Column, Integer, String, Enum
from app.database.connection import Base
from sqlalchemy.orm import relationship
import enum

class Role(str, enum.Enum):
	admin = "admin"
	staff = "staff"
	gold = "gold"
	silver = "silver"
	bronze = "bronze"
	copper = "copper"

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	phone = Column(String, nullable=False)
	email = Column(String)
	hashed_password = Column(String)
	role = Column(Enum(Role), nullable=True)

	tee_times = relationship("TeeTime", back_populates="user", cascade="all, delete-orphan")