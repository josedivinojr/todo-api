from pydantic import BaseModel

from app.models.todos import ToDoStatus


class ToDoSchema(BaseModel):
    title: str
    description: str
    status: ToDoStatus


class ToDoPublic(ToDoSchema):
    id: int


class ToDoList(BaseModel):
    todos: list[ToDoPublic]


class ToDoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: ToDoStatus | None = None
