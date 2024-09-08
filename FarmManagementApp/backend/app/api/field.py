from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud.farm import farm as farm_crud
from ..database import get_db
from ..schemas import field as field_schemas

router = APIRouter()

@router.post("/farms/{farm_id}/fields/", response_model=field_schemas.Field)
def create_field(farm_id: int, field: field_schemas.FieldCreate, db: Session = Depends(get_db)):
    return farm_crud.create_field(db=db, obj_in=field, farm_id=farm_id)

@router.get("/farms/{farm_id}/fields/", response_model=List[field_schemas.Field])
def read_fields(farm_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fields = farm_crud.get_fields(db, farm_id=farm_id, skip=skip, limit=limit)
    return fields