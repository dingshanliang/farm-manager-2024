from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..db.base_class import Base

task_field_association = Table('task_field_association', Base.metadata,
    Column('task_id', Integer, ForeignKey('tasks.id')),
    Column('field_id', Integer, ForeignKey('fields.id'))
)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String)
    farm_id = Column(Integer, ForeignKey("farms.id"))
    assignee_id = Column(Integer, ForeignKey("users.id"))  # 添加这行

    farm = relationship("Farm", back_populates="tasks")
    fields = relationship("Field", secondary=task_field_association, back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")  # 添加这行