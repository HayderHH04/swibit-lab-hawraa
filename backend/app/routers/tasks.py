import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models import Task, User
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.core.deps import get_current_user
from app.core.redis import redis_client

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    cache_key = f"tasks:user_{current_user.id}"
    cached_tasks = redis_client.get(cache_key)
    
    if cached_tasks:
        return json.loads(cached_tasks)
    if current_user.is_admin:
        tasks = db.query(Task).all()
    else:  
        tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    

    tasks_data = [TaskResponse.model_validate(task).model_dump() for task in tasks]
    
    redis_client.set(cache_key, json.dumps(tasks_data), ex=300)
    return tasks_data

@router.post("/", response_model=TaskResponse)
def create_task(task_data: TaskCreate, 
                db: Session = Depends(get_db), 
                current_user: User = Depends(get_current_user)):
    new_task = Task(**task_data.model_dump(), owner_id=current_user.id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    redis_client.delete(f"tasks:user_{current_user.id}")
    return new_task

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    
    redis_client.delete(f"tasks:user_{current_user.id}")
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    
    redis_client.delete(f"tasks:user_{current_user.id}")
    return {"message": "Task deleted successfully"}