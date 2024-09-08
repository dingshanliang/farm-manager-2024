from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..db.base_class import Base

planting_plan_field_association = Table('planting_plan_field_association', Base.metadata,
    Column('planting_plan_id', Integer, ForeignKey('planting_plans.id')),
    Column('field_id', Integer, ForeignKey('fields.id'))
)

class PlantingPlan(Base):
    __tablename__ = "planting_plans"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    crop_type = Column(String, index=True)
    planned_start_date = Column(Date)
    planned_end_date = Column(Date)
    expected_yield = Column(Float)
    notes = Column(String, nullable=True)

    farm = relationship("Farm", back_populates="planting_plans")
    fields = relationship("Field", secondary=planting_plan_field_association, back_populates="planting_plans")