from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..models.agri_advice import (AgriAdvice, AgriAdviceRating,
                                  AgriAdviceResponse)
from ..schemas.agri_advice import (AdviceCategory, AdviceStatus,
                                   AgriAdviceCreate, AgriAdviceRatingCreate,
                                   AgriAdviceResponseCreate, AgriAdviceUpdate)
from .base import CRUDBase


class CRUDAgriAdvice(CRUDBase[AgriAdvice, AgriAdviceCreate, AgriAdviceUpdate]):
    def get_user_agri_advices(self, db: Session, user_id: int, skip: int = 0, limit: int = 100, category: Optional[AdviceCategory] = None):
        query = db.query(self.model).filter(self.model.user_id == user_id)
        if category:
            query = query.filter(self.model.category == category)
        return query.offset(skip).limit(limit).all()

    def search_agri_advices(self, db: Session, query: str, skip: int = 0, limit: int = 100):
        return db.query(self.model).filter(
            or_(
                self.model.title.ilike(f"%{query}%"),
                self.model.description.ilike(f"%{query}%")
            ),
            self.model.status == AdviceStatus.RESOLVED
        ).offset(skip).limit(limit).all()

class CRUDAgriAdviceResponse(CRUDBase[AgriAdviceResponse, AgriAdviceResponseCreate, AgriAdviceResponseCreate]):
    def create_agri_advice_response(self, db: Session, response: AgriAdviceResponseCreate, advice_id: int, expert_id: int):
        db_response = AgriAdviceResponse(**response.dict(), advice_id=advice_id, expert_id=expert_id)
        db.add(db_response)
        db.commit()
        db.refresh(db_response)
        return db_response

class CRUDAgriAdviceRating(CRUDBase[AgriAdviceRating, AgriAdviceRatingCreate, AgriAdviceRatingCreate]):
    def create_agri_advice_rating(self, db: Session, rating: AgriAdviceRatingCreate, response_id: int, user_id: int):
        # 检查用户是否是原始提问者
        response = db.query(AgriAdviceResponse).filter(AgriAdviceResponse.id == response_id).first()
        if not response:
            raise HTTPException(status_code=404, detail="回答未找到")
        
        advice = db.query(AgriAdvice).filter(AgriAdvice.id == response.advice_id).first()
        if not advice or advice.user_id != user_id:
            raise HTTPException(status_code=403, detail="您没有权限对这个回答进行评分")
        
        # 检查用户是否已经对这个回答进行过评分
        existing_rating = db.query(self.model).filter(
            self.model.response_id == response_id,
            self.model.user_id == user_id
        ).first()
        if existing_rating:
            raise HTTPException(status_code=400, detail="您已经对这个回答进行过评分")
        
        db_rating = self.model(**rating.dict(), response_id=response_id, user_id=user_id)
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        return db_rating

agri_advice = CRUDAgriAdvice(AgriAdvice)
agri_advice_response = CRUDAgriAdviceResponse(AgriAdviceResponse)
agri_advice_rating = CRUDAgriAdviceRating(AgriAdviceRating)