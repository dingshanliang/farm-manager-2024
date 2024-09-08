from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: datetime
    status: str

class TaskCreate(TaskBase):
    farm_id: int
    field_ids: List[int]

class TaskUpdate(TaskBase):
    field_ids: Optional[List[int]] = None

class Task(TaskBase):
    id: int
    farm_id: int
    field_ids: List[int]

    class Config:
        orm_mode = True