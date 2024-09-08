from typing import List, Optional

from sqlalchemy.orm import Session

from ..models.field import Field
from ..models.planting_plan import PlantingPlan
from ..schemas.planting_plan import PlantingPlanCreate, PlantingPlanUpdate
from .base import CRUDBase


class CRUDPlantingPlan(CRUDBase[PlantingPlan, PlantingPlanCreate, PlantingPlanUpdate]):
    def create_with_fields(self, db: Session, *, obj_in: PlantingPlanCreate, field_ids: List[int]) -> PlantingPlan:
        db_obj = PlantingPlan(
            crop_type=obj_in.crop_type,
            planned_start_date=obj_in.planned_start_date,
            planned_end_date=obj_in.planned_end_date,
            expected_yield=obj_in.expected_yield,
            notes=obj_in.notes,
        )
        db_obj.fields = [db.query(Field).get(field_id) for field_id in field_ids]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: PlantingPlan, obj_in: PlantingPlanUpdate) -> PlantingPlan:
        update_data = obj_in.dict(exclude_unset=True)
        if 'field_ids' in update_data:
            field_ids = update_data.pop('field_ids')
            db_obj.fields = [db.query(Field).get(field_id) for field_id in field_ids]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_by_field(self, db: Session, *, field_id: int) -> List[PlantingPlan]:
        return db.query(PlantingPlan).filter(PlantingPlan.fields.any(id=field_id)).all()

planting_plan = CRUDPlantingPlan(PlantingPlan)