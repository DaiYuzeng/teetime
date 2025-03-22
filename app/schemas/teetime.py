from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, time
from app.models.teetime import Type, WeekDay, Status


class TeeTimeBase(BaseModel):
  type: Type
  start_date: datetime
  status: Optional[Status] = Status.waiting

class RegularTeeTimeBase(TeeTimeBase):
  player_count: int

class StandingTeeTimeBase(TeeTimeBase):
  end_date: datetime
  requested_day: WeekDay
  requested_time:time
  member_list:List[str]
  priority:Optional[int]


class RegularTeeTimeCreate(RegularTeeTimeBase):
  user_id: int

class StandingTeeTimeCreate(StandingTeeTimeBase):
  user_id: int

class RegularTeeTimeUpdate(BaseModel):
  id: int
  player_count: int
  start_date: datetime
  status: Status

class StandingTeeTimeUpdate(BaseModel):
  start_date: datetime
  end_date: datetime
  requested_day: WeekDay
  requested_time: time
  member_list: List[str]
  priority:Optional[int]
  status: Status

  model_config = ConfigDict(from_attributes=True)


class RegularTeeTimeResponse(RegularTeeTimeBase):
  id: int
  user_id: int

  model_config = ConfigDict(from_attributes=True)


class StandingTeeTimeResponse(StandingTeeTimeBase):
  id: int
  user_id: int

  model_config = ConfigDict(from_attributes=True)


class RegularTeeTimePaginatedResponse(BaseModel):
  total: int
  limit: int
  offset: int
  data: List[RegularTeeTimeResponse]

class StandingTeeTimePaginatedResponse(BaseModel):
  total: int
  limit: int
  offset: int
  data: List[StandingTeeTimeResponse]