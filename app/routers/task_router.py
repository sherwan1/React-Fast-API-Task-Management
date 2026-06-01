from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Task, User
from app.schemas import TaskRequest, TaskResponse


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()

    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    if(task_id <= 0):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task Id is not valid")
    
    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")
    
    return task

@router.post("/", response_model=TaskResponse)
def post_task(request: TaskRequest, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.id == request.user_id).first()

    if request.user_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Id is not valid")

    new_task = Task(**request.model_dump())

    if existing_user:
        try:
            db.add(new_task)
            db.commit()
            db.refresh(new_task)

            return new_task
        except Exception:
            db.rollback()

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task cannot be created")
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist so task can't be created")

@router.put("/{task_id}", response_model = TaskResponse)
def update_task(task_id: int, request: TaskRequest, db: Session = Depends(get_db)):
    if task_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task Id is not valid")
    
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task doesn't exist to update")
    
    if request.user_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User Id is not valid"
        )
    existing_user = db.query(User).filter(User.id == request.user_id).first()

    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")

    
    existing_task.name = request.name
    existing_task.description = request.description
    existing_task.completed = request.completed
    existing_task.priority = request.priority
    existing_task.due_date = request.due_date
    existing_task.user_id = request.user_id

    try:
        db.commit()
        db.refresh(existing_task)

        return existing_task
    
    except Exception:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task could not be updated")

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    if task_id <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task Id is not valid")
    
    existing_task = db.query(Task).filter(Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task doesn't exist to be deleted")

    try:
        db.delete(existing_task)
        db.commit()

        return{
            "message": f"Task {task_id} has been deleted successfully"
        }
    
    except Exception:
        db.rollback()

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Task cannot be deleted")
    
            
    
    



    




    