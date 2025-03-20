import os
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException

from app.dependencies.auth import create_access_token, create_refresh_token
from app.models.user import User
from app.schemas.auth import RefreshRequest

def login_for_access_token(db: Session, form_data: OAuth2PasswordRequestForm):
  user = db.query(User).filter(User.username == form_data.username).first()
  if not user or user.hashed_password != form_data.password:
      raise HTTPException(status_code=401, detail="Invalid username or password")

  access_token = create_access_token({"sub": str(user.id)})
  refresh_token = create_refresh_token({"sub": str(user.id)})

  return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
  }

def refresh_access_token(db: Session, refresh_data: RefreshRequest):
  REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY", "your-refresh-secret-key")
  refresh_token = refresh_data.refresh_token

  try:
    payload = jwt.decode(refresh_token, REFRESH_SECRET_KEY, algorithms=["HS256"])
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token({"sub": str(user.id)})

    return {"access_token": new_access_token, "token_type": "bearer"}

  except JWTError:
    raise HTTPException(status_code=401, detail="Invalid refresh token")