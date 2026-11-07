from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

def create_task(body: TaskSchema, db: Session):
    data = body.model_dump()
    new_task = TaskModel(
        title=data["title"],
        description=data["description"],
        is_completed=data["is_completed"],
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"Status": "Task created successfully","data": new_task}

def get_task(db: Session):
    tasks = db.query(TaskModel).all()
    return {"Status": "Success", "data": tasks}

def get_one_task(db: Session, task_id: int):
    task=db.query(TaskModel).get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        return {"Status": "Success", "data": task}

def update_task(db: Session, task_id: int, body: TaskSchema):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        body=body.model_dump()
        for field, value in body.items():
            setattr(one_task, field, value) 
        db.commit()
        db.refresh(one_task)
        return {"Status": "Task updated successfully", "data": one_task}

def delete_task(db: Session, task_id: int):
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        db.delete(one_task)
        db.commit()
        return {"Status": "Task deleted successfully"}