from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database.connection import Base
import enum

class SignatureStatus(str, enum.Enum):
	pending = "Pending"
	approved = "Approved"
	denied = "Denied"

class Signature(Base):
	__tablename__ = "signatures"

	id = Column(Integer, primary_key=True, index=True)
	candidate_user_id = Column(Integer, ForeignKey("users.id"))
	shareholder_user_id = Column(Integer, ForeignKey("users.id"))
	status = Column(Enum(SignatureStatus), default=SignatureStatus.pending)

	candidate = relationship("User", foreign_keys=[candidate_user_id], back_populates="candidate_signatures")
	shareholder = relationship("User", foreign_keys=[shareholder_user_id], back_populates="shareholder_signatures")
