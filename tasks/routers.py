from fastapi import APIRouter, Depends, HTTPException, Path, Query, Response, status
from fastapi.responses import JSONResponse
from tasks.models import TaskModel
from users.models import UserModel
from tasks.schemas import *
from sqlalchemy import select
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user




router = APIRouter(prefix="/todo",tags=["tasks"])


@router.get("/tasks", response_model=list[TaskResponse])
async def all_tasks(limit: int = Query(default=10, gt=0, le=20), db:Session = Depends(get_db),current_user : UserModel=Depends(get_current_user)):
    tasks = db.scalars(select(TaskModel).where(TaskModel.user_id == current_user.id).limit(limit)).all()
    
    if not tasks:
        raise HTTPException(status_code=404, detail="your list is empty")
    return tasks


@router.get("/task/{task_id}", response_model=TaskResponse)
async def get_one_task(task_id: int = Path(ge=1), db : Session = Depends(get_db), current_user: UserModel=Depends(get_current_user)):
    task = db.scalar(select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user.id))
    print(task)
    print(type(task))
    if not task:
        raise HTTPException(status_code=404, detail= "your task not found")
    return task



@router.post("/task", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(data: TaskCreateSchema, db: Session = Depends(get_db), current_user:UserModel=Depends(get_current_user)):
    dicdata = data.model_dump()
    dicdata["user_id"] = current_user.id
    print(dicdata)
    task_obj = TaskModel(**dicdata)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj


@router.put("/task/{task_id}", response_model=TaskResponse)
async def edit_task(data: TaskUpdateSchema, task_id: int = Path(ge=1), db:Session=Depends(get_db), current_user:UserModel=Depends(get_current_user)):
    task = db.scalar(select(TaskModel).where(TaskModel.id == task_id, TaskModel.user_id == current_user.id))
    if not task:
        raise HTTPException(status_code=404, detail="your task not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task
 

@router.delete("/task/{task_id}")
async def delete_task(task_id: int, db : Session = Depends(get_db), current_user:UserModel=Depends(get_current_user)):
    task = db.get(TaskModel, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="your task not found")
    
    if current_user.id != task.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you cant delete this task")
    
    db.delete(task)
    db.commit()

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)


    