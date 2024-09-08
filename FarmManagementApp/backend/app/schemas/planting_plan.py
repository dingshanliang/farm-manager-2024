from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from .field import CropType  # 更改这一行


class PlantingPlanBase(BaseModel):
    crop_type: CropType
    planned_start_date: date
    planned_end_date: date
    expected_yield: float
    notes: Optional[str] = None

class PlantingPlanCreate(PlantingPlanBase):
    field_ids: List[int]

class PlantingPlanUpdate(PlantingPlanBase):
    field_ids: Optional[List[int]] = None

class PlantingPlan(PlantingPlanBase):
    id: int
    field_ids: List[int]

    class Config:
        orm_mode = True