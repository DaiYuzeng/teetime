from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.teetime import TeeTime, Type
from app.schemas.teetime import RegularTeeTimeCreate, StandingTeeTimeCreate, RegularTeeTimeUpdate, StandingTeeTimeUpdate

def get_teetimes(db: Session, limit: int, offset: int):
	query = db.query(TeeTime)
	total_count = db.query(func.count(TeeTime.id)).scalar()
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

def create_teetime(data: RegularTeeTimeCreate | StandingTeeTimeCreate, db: Session):
  if data.type == Type.regular:
    return _create_regular_teetime(data, db)
  elif data.type == Type.standing:
    return _create_standing_teetime(data, db)
  else:
    raise ValueError(f"Unsupported tee time type: {data.type}")


def _create_regular_teetime(data: RegularTeeTimeCreate, db: Session):
  new_row = TeeTime(
    type=data.type,
    player_count=data.player_count,
    start_date=data.start_date,
    user_id=data.user_id
  )
  
  db.add(new_row)
  db.commit()
  db.refresh(new_row)
	
  return new_row

def _create_standing_teetime(data: StandingTeeTimeCreate, db: Session):
  new_row = TeeTime(
    type=data.type,
    start_date=data.start_date,
    end_date=data.end_date,
    requested_day=data.requested_day,
    requested_time=data.requested_time,
    member_list=data.member_list,
    user_id=data.user_id
  )
  
  db.add(new_row)
  db.commit()
  db.refresh(new_row)
	
  return new_row

def update_teetime(data: RegularTeeTimeUpdate | StandingTeeTimeUpdate, db: Session):
  if data.type == Type.regular:
    return _update_regular_teetime(data, db)
  elif data.type == Type.standing:
    return _update_standing_teetime(data, db)
  else:
    raise ValueError(f"Unsupported tee time type: {data.type}")

def _update_regular_teetime(data: RegularTeeTimeUpdate, db: Session):
	existing_data = db.query(TeeTime).filter(TeeTime.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="TeeTime not found")

	existing_data.status = data.status

	db.commit()
	db.refresh(existing_data)
	return existing_data

def _update_regular_teetime(data: StandingTeeTimeUpdate, db: Session):
	existing_data = db.query(TeeTime).filter(TeeTime.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="TeeTime not found")

	existing_data.status = data.status
	
	db.commit()
	db.refresh(existing_data)
	return existing_data



def _update_standing_teetime(data: StandingTeeTimeUpdate, db: Session):
	existing_data = db.query(TeeTime).filter(TeeTime.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="TeeTime not found")

	existing_data.status = data.status
  
	if data.priority:
		existing_data.priority = data.priority
	
	db.commit()
	db.refresh(existing_data)
	return existing_data
