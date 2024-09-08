from datetime import date
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class GeometryBase(BaseModel):
    type: str
    coordinates: List[List[float]]

class CropType(str, Enum):
    WHEAT = "小麦"
    CORN = "玉米"
    RICE = "水稻"
    SOYBEAN = "大豆"

class FieldBase(BaseModel):
    name: str
    size: float = Field(..., gt=0)
    crop_type: CropType
    geometry: GeometryBase

class FieldCreate(FieldBase):
    pass

class FieldUpdate(FieldBase):
    pass

class Field(FieldBase):
    id: int
    farm_id: int
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        # 将 GeoAlchemy2 的 geometry 对象转换为 GeoJSON 格式
        if obj.geometry:
            shape = obj.geometry.shape
            obj.geometry = GeometryBase(type=shape.geom_type, coordinates=list(shape.coords))
        return super().from_orm(obj)