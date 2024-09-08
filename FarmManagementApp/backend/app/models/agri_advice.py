import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text)
from sqlalchemy.orm import relationship

from ..db.base_class import Base


class AdviceStatus(enum.Enum):
    PENDING = "待处理"
    IN_PROGRESS = "处理中"
    RESOLVED = "已解决"

class AdviceCategory(enum.Enum):
    CROP_DISEASE = "作物病害"
    PEST_CONTROL = "虫害防治"
    FERTILIZATION = "施肥管理"
    IRRIGATION = "灌溉技术"
    SOIL_MANAGEMENT = "土壤管理"
    GENERAL = "一般问题"

class AgriAdvice(Base):
    __tablename__ = "agri_advices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, index=True)
    description = Column(Text)
    image_url = Column(String, nullable=True)
    status = Column(Enum(AdviceStatus))
    category = Column(Enum(AdviceCategory))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    user = relationship("User", back_populates="agri_advices")
    responses = relationship("AgriAdviceResponse", back_populates="advice")

class AgriAdviceResponse(Base):
    __tablename__ = "agri_advice_responses"

    id = Column(Integer, primary_key=True, index=True)
    advice_id = Column(Integer, ForeignKey("agri_advices.id"))
    expert_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    created_at = Column(DateTime)
    
    advice = relationship("AgriAdvice", back_populates="responses")
    expert = relationship("User", back_populates="expert_responses")
    ratings = relationship("AgriAdviceRating", back_populates="response")

class AgriAdviceRating(Base):
    __tablename__ = "agri_advice_ratings"

    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("agri_advice_responses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)  # 1-5 星评分
    created_at = Column(DateTime)

    response = relationship("AgriAdviceResponse", back_populates="ratings")
    user = relationship("User", back_populates="agri_advice_ratings")