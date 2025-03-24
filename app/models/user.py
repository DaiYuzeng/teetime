from sqlalchemy import Column, Integer, String, Enum
from app.database.connection import Base
from sqlalchemy.orm import relationship
import enum

class Role(str, enum.Enum):
	admin = "admin"
	staff = "staff"
	shareholder = "shareholder"
	associate = "associate"
	shareholder_spouse = "shareholder_spouse"
	associate_spouse = "associate_spouse"
	pee_wee = "pee_wee"
	junior = "junior"
	intermediate = "intermediate"
	social = "social"
	guest = "guest"

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	firstname = Column(String)
	lastname = Column(String)
	address = Column(String)
	phone = Column(String, nullable=False)
	email = Column(String)
	shareholder1_username = Column(String)
	shareholder2_username = Column(String)
	hashed_password = Column(String)
	role = Column(Enum(Role, native_enum=False), nullable=True)

	tee_times = relationship("TeeTime", back_populates="user", cascade="all, delete-orphan")
	candidate_signatures = relationship("Signature", foreign_keys="[Signature.candidate_user_id]", back_populates="candidate")
	shareholder_signatures = relationship("Signature", foreign_keys="[Signature.shareholder_user_id]", back_populates="shareholder")