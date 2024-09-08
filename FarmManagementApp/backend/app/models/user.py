from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    # 使用字符串引用而不是直接引用类
    farms = relationship("Farm", back_populates="owner")
    assigned_tasks = relationship("Task", back_populates="assignee")
    agri_advices = relationship("AgriAdvice", back_populates="user")
    expert_responses = relationship("AgriAdviceResponse", back_populates="expert")
    agri_advice_ratings = relationship("AgriAdviceRating", back_populates="user")