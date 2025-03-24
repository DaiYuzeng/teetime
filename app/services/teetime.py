from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.dependencies.access_control import get_all_or_own
from app.models.teetime import TeeTime, TeeTimeStatus, Type
from app.models.user import User
from app.schemas.teetime import TeeTimeBase, TeeTimeUpdate

def get_teetimes(db: Session, current_user, limit: int, offset: int):
	query = get_all_or_own(
		model=TeeTime,
		db=db,
		current_user=current_user,
		filter_column='user_id'
	)

	total_count = query.count()
	data = query.offset(offset).limit(limit).all()
	return {
			"total": total_count,
			"limit": limit,
			"offset": offset,
			"data": data,
	}

def get_teetime_by_id(teetime_id: int, db: Session):
	data = db.query(TeeTime).filter(TeeTime.id == teetime_id).first()
	if not data:
			raise HTTPException(status_code=404, detail="TeeTime not found")
	return data

def delete_teetime(teetime_id: int, db: Session):
	data = db.query(TeeTime).filter(TeeTime.id == teetime_id).first()
	if not data:
			raise HTTPException(status_code=404, detail="TeeTime not found")
	db.delete(data)
	db.commit()
	return {"message": "TeeTime deleted successfully"}

def create_teetime(data: TeeTimeBase, current_user, db: Session):
  if data.type == Type.regular:
    return _create_regular_teetime(data, current_user, db)
  elif data.type == Type.standing:
    return _create_standing_teetime(data, current_user, db)
  else:
    raise ValueError(f"Unsupported tee time type: {data.type}")


def _create_regular_teetime(data: TeeTimeBase, current_user: User, db: Session):
  new_row = TeeTime(
    type=data.type,
    player_count=data.player_count,
    start_date=data.start_date,
		status=TeeTimeStatus.pending,
    user_id=current_user.id
  )
  db.add(new_row)
  db.commit()
  db.refresh(new_row)
	
  return new_row

def _create_standing_teetime(data: TeeTimeBase, current_user: User, db: Session):
  new_row = TeeTime(
    type=data.type,
    start_date=data.start_date,
    end_date=data.end_date,
    requested_day=data.requested_day,
    requested_time=data.requested_time,
    member_list=data.member_list,
		status=TeeTimeStatus.pending,
    user_id=current_user.id
  )
  
  db.add(new_row)
  db.commit()
  db.refresh(new_row)
	
  return new_row

def update_teetime(data: TeeTimeUpdate, db: Session):
  if data.type == Type.regular:
    return _update_regular_teetime(data, db)
  elif data.type == Type.standing:
    return _update_standing_teetime(data, db)
  else:
    raise ValueError(f"Unsupported tee time type: {data.type}")


def _update_regular_teetime(data: TeeTimeUpdate, db: Session):
	existing_data = db.query(TeeTime).filter(TeeTime.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="TeeTime not found")

	existing_data.status = data.status
	existing_data.start_date = data.start_date
	existing_data.player_count = data.player_count
	
	db.commit()
	db.refresh(existing_data)
	return existing_data


def _update_standing_teetime(data: TeeTimeUpdate, db: Session):
	existing_data = db.query(TeeTime).filter(TeeTime.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="TeeTime not found")

	existing_data.status = data.status
	existing_data.start_date = data.start_date
	existing_data.end_date = data.end_date
	existing_data.requested_day = data.requested_day
	existing_data.requested_time = data.requested_time
	existing_data.member_list = data.member_list
  
	if data.priority:
		existing_data.priority = data.priority
	
	db.commit()
	db.refresh(existing_data)
	return existing_data
