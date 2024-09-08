from typing import Optional

from sqlalchemy.orm import Session

from ..core.security import get_password_hash
from ..models.user import User
from ..schemas.user import UserCreate
from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserCreate]):
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        db_obj = User(
            email=obj_in.email,
            hashed_password=hashed_password
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()


user = CRUDUser(User)