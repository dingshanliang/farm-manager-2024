from typing import List, Optional

from app.models.field import Field
from sqlalchemy.orm import Session

from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate
from .base import CRUDBase


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_fields(self, db: Session, *, obj_in: TaskCreate, field_ids: List[int]) -> Task:
        db_obj = Task(
            title=obj_in.title,
            description=obj_in.description,
            due_date=obj_in.due_date,
            status=obj_in.status,
            farm_id=obj_in.farm_id,
        )
        db_obj.fields = [db.query(Field).get(field_id) for field_id in field_ids]
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Task, obj_in: TaskUpdate) -> Task:
        update_data = obj_in.dict(exclude_unset=True)
        if 'field_ids' in update_data:
            field_ids = update_data.pop('field_ids')
            db_obj.fields = [db.query(Field).get(field_id) for field_id in field_ids]
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def get_multi_by_farm(self, db: Session, farm_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return db.query(self.model).filter(self.model.farm_id == farm_id).offset(skip).limit(limit).all()

task = CRUDTask(Task)