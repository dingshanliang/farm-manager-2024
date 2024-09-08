from datetime import date
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, validator

# 删除 GeometryBase 和 CropType 的导入，因为它们现在在 field.py 中

class ActivityType(str, Enum):
    PLOWING = "耕作"
    PLANTING = "种植"
    FERTILIZING = "施肥"
    IRRIGATING = "灌溉"
    HARVESTING = "收获"

class FarmBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    location: str = Field(..., min_length=1, max_length=200)
    size: float = Field(..., gt=0)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @validator('size')
    def size_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('农场大小必须大于0')
        return v

class FarmCreate(FarmBase):
    owner_id: int

class FarmUpdate(FarmBase):
    pass

class Farm(FarmBase):
    id: int
    owner_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

# 删除 FieldBase, FieldCreate, FieldUpdate, 和 Field 类，因为它们现在在 field.py 中

class FarmActivityBase(BaseModel):
    activity_type: ActivityType
    description: Optional[str] = None
    date: date

class FarmActivityCreate(FarmActivityBase):
    field_id: int

class FarmActivityUpdate(FarmActivityBase):
    pass

class FarmActivity(FarmActivityBase):
    id: int
    farm_id: int
    field_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True