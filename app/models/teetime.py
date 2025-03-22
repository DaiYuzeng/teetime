from sqlalchemy import Column, Integer, String, ARRAY, SmallInteger, DateTime, Time, Enum, ForeignKey
from app.database.connection import Base
from sqlalchemy.orm import relationship
import enum

class Type(str, enum.Enum):
	regular = "regular"
	standing = "standing"

class WeekDay(str, enum.Enum):
	monday = "Monday"
	tuesday = "Tuesday"
	wednesday = "Wednesday"
	thursday = "Thursday"
	friday = "Friday"
	saturday = "Saturday"
	sunday = "Sunday"

class Status(str, enum.Enum):
	waiting = "Waiting"
	approve = "Approve"
	cancel = "Cancel"
	deny = "Deny"
	finish = "Finish"



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
	status = Column(Enum(Status), default=Status.waiting)

	user_id = Column(Integer, ForeignKey("users.id"))
	user = relationship("User", back_populates="tee_times")