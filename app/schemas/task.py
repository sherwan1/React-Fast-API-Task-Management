from datetime import date, datetime
from pydantic import BaseModel, ConfigDict

from app.models.task_model import TaskPriority



class TaskRequest(BaseModel):
    name: str 
    description: str | None = None
    completed: bool = False
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None
    user_id: int


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str | None
    completed: bool
    priority: TaskPriority
    due_date: date | None
    created_at: datetime
    updated_at: datetime
    user_id: int

    model_config = ConfigDict(from_attributes=True)
