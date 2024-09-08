from typing import List, Optional

from app.crud.base import CRUDBase
from app.models.farm import Farm
from app.models.farm_activity import FarmActivity
from app.models.field import Field
from app.schemas.farm import FarmCreate, FarmUpdate
from app.schemas.field import FieldCreate
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload


class CRUDFarm(CRUDBase[Farm, FarmCreate, FarmUpdate]):
    def get_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Farm]:
        return (
            db.query(self.model)
            .filter(Farm.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_farm_with_fields(self, db: Session, farm_id: int) -> Optional[Farm]:
        return db.query(self.model).options(joinedload(self.model.fields)).filter(self.model.id == farm_id).first()

    def search_farms(self, db: Session, query: str, skip: int = 0, limit: int = 10) -> List[Farm]:
        return db.query(self.model).filter(
            or_(
                self.model.name.ilike(f"%{query}%"),
                self.model.location.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()

    def get_fields(self, db: Session, farm_id: int, skip: int = 0, limit: int = 100) -> List[Field]:
        return db.query(self.model.fields).filter(self.model.id == farm_id).offset(skip).limit(limit).all()

    def get_farm_activities(self, db: Session, farm_id: int, skip: int = 0, limit: int = 100) -> List[FarmActivity]:
        return db.query(self.model.activities).filter(self.model.id == farm_id).offset(skip).limit(limit).all()
    
    def create_field(self, db: Session, field: FieldCreate, farm_id: int) -> Field:
        db_field = Field(**field.dict(), farm_id=farm_id)
        db.add(db_field)
        db.commit()
        db.refresh(db_field)
        return db_field

farm = CRUDFarm(Farm)