from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.dependencies.auth import check_role, get_current_user
from app.models.user import Role, User
from app.schemas.signature import SignatureCreate, SignatureUpdate, SignatureResponse, SignaturePaginatedResponse
from app.services import signature_service

router = APIRouter()

@router.get("/signature", response_model=SignaturePaginatedResponse, dependencies=[Depends(check_role([Role.admin, Role.staff, Role.shareholder]))])
def list_signatures(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return signature_service.get_signatures(db, current_user, limit, offset)

@router.get("/signature/{id}", response_model=SignatureResponse, dependencies=[Depends(check_role([Role.admin, Role.staff, Role.shareholder]))])
def get_signature(id: int, db: Session = Depends(get_db)):
    return signature_service.get_signature_by_id(id, db)

@router.get("/signature/user/{id}", response_model=List[SignatureResponse])
def get_signature(id: int, db: Session = Depends(get_db)):
    return signature_service.get_signature_by_user_id(id, db)

@router.post("/signature", response_model=SignatureResponse, dependencies=[Depends(check_role([Role.admin, Role.staff, Role.shareholder]))])
def create_new_signature(data: SignatureCreate, db: Session = Depends(get_db)):
    return signature_service.create_signature(data, db)

@router.put("/signature/{id}", response_model=SignatureResponse, dependencies=[Depends(check_role([Role.admin, Role.staff, Role.shareholder]))])
def update_existing_signature(data: SignatureUpdate, db: Session = Depends(get_db)):
    return signature_service.update_signature(data, db)

@router.delete("/signature/{id}", dependencies=[Depends(check_role([Role.admin, Role.staff, Role.shareholder]))])
def delete_signature_by_id(id: int, db: Session = Depends(get_db)):
    return signature_service.delete_signature(id, db)
