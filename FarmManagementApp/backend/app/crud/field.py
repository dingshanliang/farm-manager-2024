from typing import Any, Dict, List, Union

from sqlalchemy.orm import Session

from ..models.field import Field
from ..schemas.field import FieldCreate, FieldUpdate
from .base import CRUDBase


class CRUDField(CRUDBase[Field, FieldCreate, FieldUpdate]):
    def create(self, db: Session, *, obj_in: FieldCreate) -> Field:
        db_obj = Field(
            farm_id=obj_in.farm_id,
            name=obj_in.name,
            size=obj_in.size,
            geometry=obj_in.geometry
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Field, obj_in: Union[FieldUpdate, Dict[str, Any]]) -> Field:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_farm(self, db: Session, *, farm_id: int) -> List[Field]:
        return db.query(Field).filter(Field.farm_id == farm_id).all()

field = CRUDField(Field)