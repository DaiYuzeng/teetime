from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from app.schemas.auth import RefreshRequest

from app.services import auth_service

router = APIRouter()

@router.post("/token", response_model=dict)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	return auth_service.login_for_access_token(db, form_data)

@router.post("/refresh", response_model=dict)
def refresh_access_token(refresh_data: RefreshRequest, db: Session = Depends(get_db)):
	return auth_service.refresh_access_token(db, refresh_data)
