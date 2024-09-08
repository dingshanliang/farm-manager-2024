from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.security import get_current_active_user
from ..crud import farm_activity as farm_activity_crud
from ..database import get_db
from ..schemas import farm_activity as farm_activity_schemas
from ..schemas.user import User as UserSchema

router = APIRouter()

@router.post("/", response_model=farm_activity_schemas.FarmActivity)
def create_activity(
    activity: farm_activity_schemas.FarmActivityCreate,
    db: Session = Depends(get_db),
    current_user: UserSchema = Depends(get_current_active_user)
):
    return farm_activity_crud.farm_activity.create_with_fields(db=db, obj_in=activity, field_ids=activity.field_ids)

@router.get("/fields/{field_id}", response_model=List[farm_activity_schemas.FarmActivity])
def read_activities_by_field(field_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    activities = farm_activity_crud.farm_activity.get_by_field(db, field_id=field_id, skip=skip, limit=limit)
    return activities

@router.get("/{activity_id}", response_model=farm_activity_schemas.FarmActivity)
def read_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = farm_activity_crud.farm_activity.get(db, id=activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="农事活动未找到")
    return activity

@router.put("/{activity_id}", response_model=farm_activity_schemas.FarmActivity)
def update_activity(
    activity_id: int,
    activity: farm_activity_schemas.FarmActivityUpdate,
    db: Session = Depends(get_db)
):
    db_activity = farm_activity_crud.farm_activity.get(db, id=activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="农事活动未找到")
    updated_activity = farm_activity_crud.farm_activity.update(db, db_obj=db_activity, obj_in=activity)
    return updated_activity

@router.delete("/{activity_id}", response_model=farm_activity_schemas.FarmActivity)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity = farm_activity_crud.farm_activity.remove(db, id=activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="农事活动未找到")
    return activity