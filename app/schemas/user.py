from datetime import datetime
from pydantic import BaseModel, ConfigDict

from app.schemas.task import TaskRequest, TaskResponse

class UserRequest(BaseModel):
    name: str
    email: str
    password: str



class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
    tasks: list [TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
