from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import planting_plan as planting_plan_crud
from ..database import get_db
from ..schemas import planting_plan as planting_plan_schemas

router = APIRouter()

@router.post("/farms/{farm_id}/planting-plans/", response_model=planting_plan_schemas.PlantingPlan)
def create_planting_plan(farm_id: int, plan: planting_plan_schemas.PlantingPlanCreate, db: Session = Depends(get_db)):
    return planting_plan_crud.planting_plan.create(db=db, obj_in=plan, farm_id=farm_id)

@router.get("/farms/{farm_id}/planting-plans/", response_model=List[planting_plan_schemas.PlantingPlan])
def read_planting_plans(farm_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    plans = planting_plan_crud.planting_plan.get_by_farm(db, farm_id=farm_id, skip=skip, limit=limit)
    return plans

@router.get("/planting-plans/{plan_id}", response_model=planting_plan_schemas.PlantingPlan)
def read_planting_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.planting_plan.get(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan

@router.put("/planting-plans/{plan_id}", response_model=planting_plan_schemas.PlantingPlan)
def update_planting_plan(plan_id: int, plan: planting_plan_schemas.PlantingPlanUpdate, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.planting_plan.update(db, db_obj=planting_plan_crud.planting_plan.get(db, id=plan_id), obj_in=plan)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan

@router.delete("/planting-plans/{plan_id}", response_model=planting_plan_schemas.PlantingPlan)
def delete_planting_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = planting_plan_crud.planting_plan.remove(db, id=plan_id)
    if db_plan is None:
        raise HTTPException(status_code=404, detail="种植计划未找到")
    return db_plan