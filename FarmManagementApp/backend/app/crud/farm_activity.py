from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.farm_activity import FarmActivity
from ..models.field import Field
from ..schemas.farm_activity import FarmActivityCreate, FarmActivityUpdate
from .base import CRUDBase


class CRUDFarmActivity(CRUDBase[FarmActivity, FarmActivityCreate, FarmActivityUpdate]):
    def create_with_fields(self, db: Session, *, obj_in: FarmActivityCreate, field_ids: List[int]) -> FarmActivity:
        db_obj = FarmActivity(
            activity_type=obj_in.activity_type,
            description=obj_in.description,
            date=obj_in.date
        )
        db_obj.fields = db.query(Field).filter(Field.id.in_(field_ids)).all()
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: FarmActivity, obj_in: FarmActivityUpdate) -> FarmActivity:
        update_data = obj_in.dict(exclude_unset=True)
        if 'field_ids' in update_data:
            field_ids = update_data.pop('field_ids')
            db_obj.fields = [db.query(Field).get(field_id) for field_id in field_ids]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_field(self, db: Session, *, field_id: int, skip: int = 0, limit: int = 100) -> List[FarmActivity]:
        return (
            db.query(self.model)
            .filter(self.model.fields.any(id=field_id))
            .offset(skip)
            .limit(limit)
            .all()
        )

farm_activity = CRUDFarmActivity(FarmActivity)