from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class AdviceStatus(str, Enum):
    PENDING = "待处理"
    IN_PROGRESS = "处理中"
    RESOLVED = "已解决"

class AdviceCategory(str, Enum):
    CROP_DISEASE = "作物病害"
    PEST_CONTROL = "虫害防治"
    FERTILIZATION = "施肥管理"
    IRRIGATION = "灌溉技术"
    SOIL_MANAGEMENT = "土壤管理"
    GENERAL = "一般问题"

class AgriAdviceBase(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None
    category: AdviceCategory = AdviceCategory.GENERAL

class AgriAdviceCreate(AgriAdviceBase):
    pass

class AgriAdviceUpdate(BaseModel):
    status: AdviceStatus

class AgriAdviceResponseBase(BaseModel):
    content: str

class AgriAdviceResponseCreate(AgriAdviceResponseBase):
    pass

class AgriAdviceRatingBase(BaseModel):
    rating: int

class AgriAdviceRatingCreate(AgriAdviceRatingBase):
    pass

class AgriAdviceRating(AgriAdviceRatingBase):
    id: int
    response_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AgriAdviceResponse(AgriAdviceResponseBase):
    id: int
    advice_id: int
    expert_id: int
    created_at: datetime
    ratings: List[AgriAdviceRating] = []

    class Config:
        from_attributes = True

class AgriAdvice(AgriAdviceBase):
    id: int
    user_id: int
    status: AdviceStatus
    created_at: datetime
    updated_at: datetime
    responses: List[AgriAdviceResponse] = []

    class Config:
        from_attributes = True