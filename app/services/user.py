from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.user import User, Role
from app.schemas.signature import SignatureCreate
from app.schemas.user import UserCreate, UserUpdate
from app.services.signature import create_signature

def get_users(db: Session, limit: int, offset: int):
	query = db.query(User)
	total_count = db.query(func.count(User.id)).scalar()
	users = query.offset(offset).limit(limit).all()
	return {
		"total": total_count,
		"limit": limit,
		"offset": offset,
		"data": users,
	}

def get_user_by_id(user_id: int, db: Session):
	user = db.query(User).filter(User.id == user_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	return user

def delete_user(user_id: int, db: Session):
	user = db.query(User).filter(User.id == user_id).first()
	if not user:
		raise HTTPException(status_code=404, detail="User not found")
	db.delete(user)
	db.commit()
	return {"message": "User deleted successfully"}

def register_user(user: UserCreate, db: Session):
	existing_user = db.query(User).filter(User.username == user.username).first()
	if existing_user:
		raise HTTPException(status_code=400, detail="Username already exists")

	new_user = User(
		firstname = user.firstname,
		lastname = user.lastname,
		address = user.address,
		username = user.username,
		shareholder1_username = user.shareholder1_username,
		shareholder2_username = user.shareholder2_username,
		phone = user.phone,
		email = user.email,
		hashed_password = user.hashed_password
	)
	
	db.add(new_user)
	db.flush()

	shareholder1 = db.query(User).filter_by(username=user.shareholder1_username).first()
	shareholder2 = db.query(User).filter_by(username=user.shareholder2_username).first()

	if not shareholder1 or not shareholder2:
		raise HTTPException(status_code=400, detail="Invalid shareholder usernames")
	
	create_signature(SignatureCreate(candidate_user_id=new_user.id, shareholder_user_id=shareholder1.id), db)
	create_signature(SignatureCreate(candidate_user_id=new_user.id, shareholder_user_id=shareholder2.id), db)

	db.commit()
	db.refresh(new_user)
	return new_user

def update_user(user_update: UserUpdate, db: Session):
	existing_user = db.query(User).filter(User.id == user_update.id).first()
	if not existing_user:
		raise HTTPException(status_code=404, detail="User not found")

	existing_user.firstname = user_update.firstname
	existing_user.lastname = user_update.lastname
	existing_user.address = user_update.address
	existing_user.phone = user_update.phone
	existing_user.email = user_update.email
	existing_user.role = Role(user_update.role)

	db.commit()
	db.refresh(existing_user)
	return existing_user
