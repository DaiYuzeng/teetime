from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.services import user_service
from app.database.session import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserPaginatedResponse

router = APIRouter()

@router.get("/user", response_model=UserPaginatedResponse)
def get_users(db: Session = Depends(get_db), limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
	return user_service.get_users(db=db, limit=limit, offset=offset)

@router.get("/user/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
	return user_service.get_user_by_id(user_id, db)

@router.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
	return user_service.delete_user(user_id, db)

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
	return user_service.register_user(user, db)

@router.put("/user/{user_id}", response_model=UserResponse)
def update_user(user_update: UserUpdate, db: Session = Depends(get_db)):
	return user_service.update_user(user_update, db)
