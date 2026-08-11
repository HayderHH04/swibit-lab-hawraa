from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"
    owner_id: int


class TaskUpdate(BaseModel):
    title: str
    description: str | None = None
    priority: str
    completed: bool


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    priority: str
    completed: bool
    owner_id: int

    model_config = {
        "from_attributes": True
    }