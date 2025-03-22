from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services import teetime_service
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserPaginatedResponse

router = APIRouter()

@router.get("/teetime", response_model=UserPaginatedResponse)
def get_teetimes(db: Session = Depends(get_db), limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
	return teetime_service.get_teetimes(db=db, limit=limit, offset=offset)

@router.get("/teetime/{id}", response_model=UserResponse)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
	return teetime_service.get_teetime_by_id(id, db)

@router.delete("/teetime/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
	return teetime_service.delete_teetime(id, db)

@router.post("/teetime", response_model=UserResponse)
def register_user(data: UserCreate, db: Session = Depends(get_db)):
	return teetime_service.create_teetime(data, db)

@router.put("/teetime/{id}", response_model=UserResponse)
def update_user(data: UserUpdate, db: Session = Depends(get_db)):
	return teetime_service.update_teetime(data, db)
