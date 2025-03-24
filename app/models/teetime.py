from sqlalchemy import Column, Integer, String, ARRAY, SmallInteger, DateTime, Time, Enum, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship
import enum

class Type(str, enum.Enum):
	regular = "Regular"
	standing = "Standing"

class WeekDay(str, enum.Enum):
	monday = "Monday"
	tuesday = "Tuesday"
	wednesday = "Wednesday"
	thursday = "Thursday"
	friday = "Friday"
	saturday = "Saturday"
	sunday = "Sunday"

class TeeTimeStatus(str, enum.Enum):
	pending = "Pending"
	approved = "Approved"
	denied = "Denied"



class TeeTime(Base):
	__tablename__ = "teetimes"

	id = Column(Integer, primary_key=True, index=True)
	type = Column(Enum(Type), default=Type.regular)
	player_count = Column(SmallInteger)
	start_date = Column(DateTime)
	end_date = Column(DateTime, nullable=True)
	requested_day = Column(Enum(WeekDay), nullable=True)
	requested_time = Column((Time), nullable=True)
	member_list = Column(ARRAY(String), nullable=True)
	priority = Column(SmallInteger, nullable=True)
	status = Column(Enum(TeeTimeStatus, name="teetimestatus", native_enum=False), default=TeeTimeStatus.pending)

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="tee_times")