from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional, List
from app.models.signature import SignatureStatus


class SignatureCreate(BaseModel):
  candidate_user_id: int
  shareholder_user_id: int
  status: Optional[SignatureStatus] = SignatureStatus.pending

class SignatureUpdate(BaseModel):
  id: int
  candidate_user_id: int
  shareholder_user_id: int
  status: SignatureStatus


class SignatureResponse(SignatureCreate):
  id: int
  candidate_username: str
  shareholder_username: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)

class SignaturePaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List[SignatureResponse]