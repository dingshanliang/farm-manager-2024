from sqlalchemy import Column, Enum, Float, Integer, String

from .base import Base
from .farm import CropType


class CropResource(Base):
    __tablename__ = "crop_resources"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(Enum(CropType), unique=True)
    seed_per_hectare = Column(Float)  # 每公顷所需种子量(千克)
    fertilizer_per_hectare = Column(Float)  # 每公顷所需肥料量(千克)
    water_per_hectare = Column(Float)  # 每公顷所需水量(立方米)