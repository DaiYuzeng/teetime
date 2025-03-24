from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, time
from app.models.teetime import Type, WeekDay, TeeTimeStatus


class TeeTimeBase(BaseModel):
  type: Type
  start_date: datetime
  player_count: Optional[int] = None
  end_date: Optional[datetime] = None
  requested_day: Optional[WeekDay] = None
  requested_time:Optional[time] = None
  member_list:Optional[List[str]] = None
  priority:Optional[int] = None

class TeeTimeUpdate(TeeTimeBase):
  id: int
  status: TeeTimeStatus

class TeeTimeResponse(TeeTimeBase):
  id: int
  user_id: int
  status: TeeTimeStatus

  model_config = ConfigDict(from_attributes=True)


class TeeTimePaginatedResponse(BaseModel):
  total: int
  limit: int
  offset: int
  data: List[TeeTimeResponse]
