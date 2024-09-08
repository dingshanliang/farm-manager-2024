from sqlalchemy import Column, Date, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..db.base_class import Base
from .farm import ActivityType

# 创建多对多关系的中间表
activity_field_association = Table('activity_field', Base.metadata,
    Column('activity_id', Integer, ForeignKey('farm_activities.id')),
    Column('field_id', Integer, ForeignKey('fields.id'))
)

class FarmActivity(Base):
    __tablename__ = "farm_activities"

    id = Column(Integer, primary_key=True, index=True)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    activity_type = Column(Enum(ActivityType))
    description = Column(String)
    date = Column(Date)

    farm = relationship("Farm", back_populates="activities")
    fields = relationship("Field", secondary=activity_field_association, back_populates="activities")