from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.models.signature import Signature, SignatureStatus
from app.schemas.signature import SignatureCreate, SignatureUpdate

def get_signatures(db: Session, limit: int, offset: int):
	query = db.query(Signature)
	total_count = db.query(func.count(Signature.id)).scalar()
	data = query.offset(offset).limit(limit).all()
	return {
		"total": total_count,
		"limit": limit,
		"offset": offset,
		"data": data,
	}

def get_signature_by_id(id: int, db: Session):
	data = db.query(Signature).filter(Signature.id == id).first()
	if not data:
		raise HTTPException(status_code=404, detail="Application not found")
	return data

def delete_signature(id: int, db: Session):
	data = db.query(Signature).filter(Signature.id == id).first()
	if not data:
		raise HTTPException(status_code=404, detail="Application not found")
	db.delete(data)
	db.commit()
	return {"message": "Application deleted successfully"}

def create_signature(data: SignatureCreate, db: Session):
	new_row = Signature(
		candidate_user_id=data.candidate_user_id,
		shareholder_user_id=data.shareholder_user_id,
		status=data.status
	)
	db.add(new_row)
	db.commit()
	db.refresh(new_row)
	return new_row

def update_signature(data: SignatureUpdate, db: Session):
	existing_data = db.query(Signature).filter(Signature.id == data.id).first()
	if not existing_data:
		raise HTTPException(status_code=404, detail="Application not found")

	existing_data.status = data.status

	db.commit()
	db.refresh(existing_data)
	return existing_data
