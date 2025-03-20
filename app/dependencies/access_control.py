from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_current_user
from app.models.user import User, Role

def get_all_or_own(
    model, 
    db: Session, 
    current_user: User, 
    roles: list[Role] = None,
    filter_column=None
):
    if roles is None:  
        roles = [Role.admin]

    if current_user.role in roles:
        return db.query(model)

    if not filter_column:
        raise ValueError("filter_column must be provided for non-admin users")

    if not hasattr(model, filter_column):
        raise ValueError(f"Invalid filter_column: {filter_column} does not exist in {model.__name__}")

    return db.query(model).filter(getattr(model, filter_column) == current_user.id)

