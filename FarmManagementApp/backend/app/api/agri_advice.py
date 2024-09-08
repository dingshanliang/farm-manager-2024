from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..crud import agri_advice as agri_advice_crud
from ..database import get_db
from ..schemas import agri_advice as agri_advice_schemas
from ..schemas.user import User as UserSchema

router = APIRouter()

@router.post("/", response_model=agri_advice_schemas.AgriAdvice)
def create_agri_advice(
    advice: agri_advice_schemas.AgriAdviceCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    return agri_advice_crud.create_agri_advice(db=db, advice=advice, user_id=current_user.id)

@router.get("/", response_model=List[agri_advice_schemas.AgriAdvice])
def read_agri_advices(
    skip: int = 0,
    limit: int = 100,
    category: Optional[agri_advice_schemas.AdviceCategory] = None,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    advices = agri_advice_crud.get_user_agri_advices(db, user_id=current_user.id, skip=skip, limit=limit, category=category)
    return advices

@router.get("/search", response_model=List[agri_advice_schemas.AgriAdvice])
def search_agri_advices(
    query: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    advices = agri_advice_crud.search_agri_advices(db, query=query, skip=skip, limit=limit)
    return advices

@router.get("/{advice_id}", response_model=agri_advice_schemas.AgriAdvice)
def read_agri_advice(advice_id: int, db: Session = Depends(get_db)):
    db_advice = agri_advice_crud.get_agri_advice(db, advice_id=advice_id)
    if db_advice is None:
        raise HTTPException(status_code=404, detail="农技指导问题未找���")
    return db_advice

@router.put("/{advice_id}", response_model=agri_advice_schemas.AgriAdvice)
def update_agri_advice(advice_id: int, advice: agri_advice_schemas.AgriAdviceUpdate, db: Session = Depends(get_db)):
    db_advice = agri_advice_crud.update_agri_advice(db, advice_id=advice_id, advice=advice)
    if db_advice is None:
        raise HTTPException(status_code=404, detail="农技指导问题未找到")
    return db_advice

@router.post("/{advice_id}/responses/", response_model=agri_advice_schemas.AgriAdviceResponse)
def create_agri_advice_response(advice_id: int, response: agri_advice_schemas.AgriAdviceResponseCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_active_user)):
    return agri_advice_crud.create_agri_advice_response(db=db, response=response, advice_id=advice_id, expert_id=current_user.id)

@router.post("/{advice_id}/responses/{response_id}/rate", response_model=agri_advice_schemas.AgriAdviceRating)
def rate_agri_advice_response(
    advice_id: int,
    response_id: int,
    rating: agri_advice_schemas.AgriAdviceRatingCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    db_advice = agri_advice_crud.get_agri_advice(db, advice_id=advice_id)
    if not db_advice:
        raise HTTPException(status_code=404, detail="农技指导问题未��到")
    
    db_response = agri_advice_crud.get_agri_advice_response(db, response_id=response_id)
    if not db_response or db_response.advice_id != advice_id:
        raise HTTPException(status_code=404, detail="回答未找到")
    
    if db_advice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限对这个回答进行评分")
    
    try:
        return agri_advice_crud.create_agri_advice_rating(db=db, rating=rating, response_id=response_id, user_id=current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))