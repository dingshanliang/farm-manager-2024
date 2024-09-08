from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.orm import Session

from ..core.exceptions import (ActivityNotFoundException,
                               FarmNotFoundException, FieldNotFoundException)
from ..core.logger import main_logger
from ..core.security import get_current_active_user
from ..crud import agri_advice as agri_advice_crud
from ..crud.farm import farm as farm_crud
from ..crud.planting_plan import planting_plan as planting_plan_crud
from ..crud.task import task as task_crud
from ..crud.weather import weather as weather_crud
from ..database import get_db
from ..models import farm as farm_models
from ..schemas import agri_advice as agri_advice_schemas
from ..schemas import farm as farm_schemas
from ..schemas import task as task_schemas
from ..schemas import weather as weather_schemas
from ..schemas.common import PaginatedResponse
from ..schemas.planting_plan import (PlantingPlan, PlantingPlanCreate,
                                     PlantingPlanUpdate)
from ..schemas.user import User as UserSchema

router = APIRouter()

@router.post("/farms/", response_model=farm_schemas.Farm)
def create_farm(farm: farm_schemas.FarmCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_active_user)):
    new_farm = farm_crud.create(db=db, obj_in=farm, owner_id=current_user.id)
    main_logger.info(f"用户 {current_user.id} 创建了新农场: {new_farm.id}")
    return new_farm

@router.get("/farms/", response_model=PaginatedResponse[farm_schemas.Farm])
def read_farms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    farms = farm_crud.get_multi(db, skip=skip, limit=limit)
    total = farm_crud.get_total(db)
    return PaginatedResponse(items=farms, total=total, skip=skip, limit=limit)

@router.get("/farms/{farm_id}", response_model=farm_schemas.Farm)
@cache(expire=60)
def read_farm(farm_id: int, db: Session = Depends(get_db)):
    db_farm = farm_crud.get(db, id=farm_id)
    if db_farm is None:
        raise FarmNotFoundException(farm_id)
    return db_farm

@router.put("/farms/{farm_id}", response_model=farm_schemas.Farm)
def update_farm(farm_id: int, farm: farm_schemas.FarmUpdate, db: Session = Depends(get_db)):
    db_farm = farm_crud.update(db, db_obj=farm_crud.get(db, id=farm_id), obj_in=farm)
    if db_farm is None:
        raise HTTPException(status_code=404, detail="农场未找到")
    return db_farm

@router.delete("/farms/{farm_id}", response_model=farm_schemas.Farm)
def delete_farm(farm_id: int, db: Session = Depends(get_db)):
    db_farm = farm_crud.remove(db, id=farm_id)
    if db_farm is None:
        raise HTTPException(status_code=404, detail="农场未找到")
    return db_farm

# 天气预报集成
@router.get("/farms/{farm_id}/weather/", response_model=List[weather_schemas.WeatherForecast])
def read_weather_forecasts(farm_id: int, skip: int = 0, limit: int = 7, db: Session = Depends(get_db)):
    forecasts = weather_crud.get_by_farm(db, farm_id=farm_id, skip=skip, limit=limit)
    return forecasts

# 任务分配系统
@router.post("/farms/{farm_id}/tasks/", response_model=task_schemas.Task)
def create_task(farm_id: int, task: task_schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create(db=db, obj_in=task)

@router.get("/farms/{farm_id}/tasks/", response_model=List[task_schemas.Task])
def read_tasks(farm_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = task_crud.get_by_farm(db, farm_id=farm_id, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=task_schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get(db, id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task

@router.put("/tasks/{task_id}", response_model=task_schemas.Task)
def update_task(task_id: int, task: task_schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_crud.update(db, db_obj=task_crud.get(db, id=task_id), obj_in=task)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task

@router.delete("/tasks/{task_id}", response_model=task_schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.remove(db, id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task

# 种植计划相关的路由
@router.post("/farms/{farm_id}/planting-plans/", response_model=PlantingPlan)
def create_planting_plan(farm_id: int, plan: PlantingPlanCreate, db: Session = Depends(get_db)):
    try:
        db_plan, resource_requirements, tasks = planting_plan_crud.create_planting_plan(db=db, obj_in=plan)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "planting_plan": db_plan,
        "resource_requirements": resource_requirements,
        "generated_tasks": tasks
    }

@router.get("/farms/{farm_id}/planting-plans/", response_model=List[PlantingPlan])
def read_planting_plans(farm_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = planting_plan_crud.get_by_farm(db, farm_id=farm_id, skip=skip, limit=limit)
    return plans

@router.get("/planting-plans/{plan_id}", response_model=PlantingPlan)
def read_planting_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.get(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan

@router.put("/planting-plans/{plan_id}", response_model=PlantingPlan)
def update_planting_plan(plan_id: int, plan: PlantingPlanUpdate, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.update(db, db_obj=planting_plan_crud.get(db, id=plan_id), obj_in=plan)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan

@router.delete("/planting-plans/{plan_id}", response_model=PlantingPlan)
def delete_planting_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.remove(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan

# 农技指导相关的路由
@router.post("/agri-advices/", response_model=agri_advice_schemas.AgriAdvice)
def create_agri_advice(
    advice: agri_advice_schemas.AgriAdviceCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    return agri_advice_crud.create(db=db, obj_in=advice, user_id=current_user.id)

@router.get("/agri-advices/", response_model=List[agri_advice_schemas.AgriAdvice])
def read_agri_advices(
    skip: int = 0,
    limit: int = 100,
    category: Optional[agri_advice_schemas.AdviceCategory] = None,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    advices = agri_advice_crud.get_user_agri_advices(db, user_id=current_user.id, skip=skip, limit=limit, category=category)
    return advices

@router.get("/agri-advices/search", response_model=List[agri_advice_schemas.AgriAdvice])
def search_agri_advices(
    query: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    advices = agri_advice_crud.search_agri_advices(db, query=query, skip=skip, limit=limit)
    return advices

@router.get("/agri-advices/{advice_id}", response_model=agri_advice_schemas.AgriAdvice)
def read_agri_advice(advice_id: int, db: Session = Depends(get_db)):
    db_advice = agri_advice_crud.get(db, id=advice_id)
    if db_advice is None:
        raise HTTPException(status_code=404, detail="农技指导问题未找到")
    return db_advice

@router.put("/agri-advices/{advice_id}", response_model=agri_advice_schemas.AgriAdvice)
def update_agri_advice(advice_id: int, advice: agri_advice_schemas.AgriAdviceUpdate, db: Session = Depends(get_db)):
    db_advice = agri_advice_crud.update(db, db_obj=agri_advice_crud.get(db, id=advice_id), obj_in=advice)
    if db_advice is None:
        raise HTTPException(status_code=404, detail="农技指导问题未找到")
    return db_advice

@router.post("/agri-advices/{advice_id}/responses/", response_model=agri_advice_schemas.AgriAdviceResponse)
def create_agri_advice_response(advice_id: int, response: agri_advice_schemas.AgriAdviceResponseCreate, db: Session = Depends(get_db), current_user: UserSchema = Depends(get_current_active_user)):
    return agri_advice_crud.agri_advice_response.create_agri_advice_response(db=db, response=response, advice_id=advice_id, expert_id=current_user.id)

@router.post("/agri-advices/{advice_id}/responses/{response_id}/rate", response_model=agri_advice_schemas.AgriAdviceRating)
def rate_agri_advice_response(
    advice_id: int,
    response_id: int,
    rating: agri_advice_schemas.AgriAdviceRatingCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    db_advice = agri_advice_crud.get(db, id=advice_id)
    if not db_advice:
        raise HTTPException(status_code=404, detail="农技指导问题未找到")
    
    db_response = agri_advice_crud.agri_advice_response.get(db, id=response_id)
    if not db_response or db_response.advice_id != advice_id:
        raise HTTPException(status_code=404, detail="回答未找到")
    
    if db_advice.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="您没有权限对这个回答进行评分")
    
    try:
        return agri_advice_crud.agri_advice_rating.create_agri_advice_rating(db=db, rating=rating, response_id=response_id, user_id=current_user.id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))