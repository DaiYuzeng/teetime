from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies.auth import check_role, get_current_user
from app.models.user import Role, User
from app.services import teetime_service
from app.database.session import get_db
from app.schemas.teetime import TeeTimePaginatedResponse, TeeTimeResponse, TeeTimeBase, TeeTimeUpdate

router = APIRouter()

ALLOWED_ROLES_EXCEPT_SOCIAL = [role for role in Role if role != Role.social]

@router.get("/teetime", response_model=TeeTimePaginatedResponse, dependencies=[Depends(check_role(ALLOWED_ROLES_EXCEPT_SOCIAL))])
def get_teetimes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0)):
	return teetime_service.get_teetimes(db=db, current_user=current_user, limit=limit, offset=offset)

@router.get("/teetime/{id}", response_model=TeeTimeResponse, dependencies=[Depends(check_role(ALLOWED_ROLES_EXCEPT_SOCIAL))])
def get_teetime_by_id(id: int, db: Session = Depends(get_db)):
	return teetime_service.get_teetime_by_id(id, db)

@router.delete("/teetime/{id}", dependencies=[Depends(check_role(ALLOWED_ROLES_EXCEPT_SOCIAL))])
def delete_teetime(id: int, db: Session = Depends(get_db)):
	return teetime_service.delete_teetime(id, db)

@router.post("/teetime", response_model=TeeTimeResponse, dependencies=[Depends(check_role(ALLOWED_ROLES_EXCEPT_SOCIAL))])
def create_teetime(data: TeeTimeBase, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
	return teetime_service.create_teetime(data, current_user, db)

@router.put("/teetime/{id}", response_model=TeeTimeResponse, dependencies=[Depends(check_role(ALLOWED_ROLES_EXCEPT_SOCIAL))])
def update_teetime(data: TeeTimeUpdate, db: Session = Depends(get_db)):
	return teetime_service.update_teetime(data, db)
