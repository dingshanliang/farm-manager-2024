from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from .farm import ActivityType


class FarmActivityBase(BaseModel):
    activity_type: ActivityType
    description: Optional[str] = None
    date: date

class FarmActivityCreate(FarmActivityBase):
    field_ids: List[int]

class FarmActivityUpdate(FarmActivityBase):
    field_ids: Optional[List[int]] = None

class FarmActivity(FarmActivityBase):
    id: int
    created_at: date
    updated_at: date
    field_ids: List[int]

    class Config:
        from_attributes = True