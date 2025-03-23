from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
from models.signature import SignatureStatus


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

  model_config = ConfigDict(from_attributes=True)