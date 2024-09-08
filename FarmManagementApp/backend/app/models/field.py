from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..db.base_class import Base
from .farm_activity import activity_field_association


class Field(Base):
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    name = Column(String, index=True)
    size = Column(Float)
    geometry = Column(Geometry(geometry_type='POLYGON', srid=4326))

    # 使用字符串引用
    farm = relationship("Farm", back_populates="fields")
    tasks = relationship("Task", secondary="task_field_association", back_populates="fields")
    planting_plans = relationship("PlantingPlan", secondary="planting_plan_field_association", back_populates="fields")
    activities = relationship("FarmActivity", secondary=activity_field_association, back_populates="fields")