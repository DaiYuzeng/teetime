import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException

from app.dependencies.access_control import get_all_or_own
from app.models.signature import Signature
from app.models.user import Role, User
from app.schemas.signature import SignatureCreate, SignatureUpdate

from app.schemas.signature import SignatureResponse

def get_signatures(db: Session, current_user: User, limit: int, offset: int):
	query = get_all_or_own(
		model=Signature,
		db=db,
		current_user=current_user,
		filter_column='shareholder_user_id'
	).options(
		joinedload(Signature.candidate)
	)

	total_count = query.count()
	signatures = query.offset(offset).limit(limit).all()

	response_data = [
		SignatureResponse(
			id=sig.id,
			candidate_user_id=sig.candidate_user_id,
			shareholder_user_id=sig.shareholder_user_id,
			status=sig.status,
			candidate_username=sig.candidate.username if sig.candidate else None
		)
		for sig in signatures
	]

	return {
		"total": total_count,
		"limit": limit,
		"offset": offset,
		"data": response_data
	}

def get_signature_by_id(id: int, db: Session):
	sig = db.query(Signature).options(sqlalchemy.orm.joinedload(Signature.candidate)).filter(Signature.id == id).first()
	if not sig:
		raise HTTPException(status_code=404, detail="Application not found")

	return SignatureResponse(
		id=sig.id,
		candidate_user_id=sig.candidate_user_id,
		shareholder_user_id=sig.shareholder_user_id,
		status=sig.status,
		candidate_username=sig.candidate.username if sig.candidate else None
	)

def get_signature_by_user_id(user_id: int, db: Session):
	signatures = db.query(Signature)\
		.options(joinedload(Signature.candidate))\
		.options(joinedload(Signature.shareholder))\
		.filter(Signature.candidate_user_id == user_id)\
		.all()

	if not signatures:
		raise HTTPException(status_code=404, detail="No signature records found for this user")

	return [
		SignatureResponse(
			id=sig.id,
			candidate_user_id=sig.candidate_user_id,
			shareholder_user_id=sig.shareholder_user_id,
			status=sig.status,
			candidate_username=sig.candidate.username if sig.candidate else None,
			shareholder_username=sig.shareholder.username if sig.shareholder else None
		) for sig in signatures
	]

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

from sqlalchemy.orm import joinedload
from app.schemas.signature import SignatureResponse

def update_signature(data: SignatureUpdate, db: Session):
	existing_data = db.query(Signature) \
		.options(joinedload(Signature.candidate)) \
		.filter(Signature.id == data.id).first()

	if not existing_data:
		raise HTTPException(status_code=404, detail="Application not found")

	existing_data.status = data.status

	db.commit()
	db.refresh(existing_data)

	return SignatureResponse(
		id=existing_data.id,
		candidate_user_id=existing_data.candidate_user_id,
		shareholder_user_id=existing_data.shareholder_user_id,
		status=existing_data.status,
		candidate_username=existing_data.candidate.username if existing_data.candidate else None
	)

