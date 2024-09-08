from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..crud import task as task_crud
from ..database import get_db
from ..schemas import task as task_schemas

router = APIRouter()

@router.post("/tasks/", response_model=task_schemas.Task)
def create_task(task: task_schemas.TaskCreate, db: Session = Depends(get_db)):
    return task_crud.create_with_fields(db=db, obj_in=task, field_ids=task.field_ids)

@router.get("/farms/{farm_id}/tasks/", response_model=List[task_schemas.Task])
def read_tasks(farm_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = task_crud.get_multi_by_farm(db, farm_id=farm_id, skip=skip, limit=limit)
    return tasks

@router.get("/tasks/{task_id}", response_model=task_schemas.Task)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.get(db, id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task

@router.put("/tasks/{task_id}", response_model=task_schemas.Task)
def update_task(task_id: int, task: task_schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = task_crud.get(db, id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return task_crud.update(db, db_obj=db_task, obj_in=task)

@router.delete("/tasks/{task_id}", response_model=task_schemas.Task)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = task_crud.remove(db, id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="任务未找到")
    return db_task