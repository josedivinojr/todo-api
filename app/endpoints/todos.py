from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.todos import ToDo, ToDoStatus
from app.models.users import User
from app.schemas.message import Message
from app.schemas.todos import ToDoList, ToDoPublic, ToDoSchema, ToDoUpdate
from app.security import get_current_user

router = APIRouter(prefix='/todos', tags=['todos'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', response_model=ToDoPublic)
def create_todo(todo: ToDoSchema, session: T_Session, user: T_CurrentUser):
    db_todo = ToDo(
        title=todo.title,
        description=todo.description,
        status=todo.status,
        user_id=user.id,
    )
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo


# TODO: refactor to a class ToDoListFilters
@router.get('/', response_model=ToDoList)
def list_todos(  # noqa
    session: T_Session,
    user: T_CurrentUser,
    title: str | None = None,
    description: str | None = None,
    status: ToDoStatus | None = None,
    limit: int | None = None,
    offset: int | None = None,
):
    query = select(ToDo).where(ToDo.user_id == user.id)

    if title:
        query = query.filter(ToDo.title.contains(title))

    if description:
        query = query.filter(ToDo.description.contains(description))

    if status:
        query = query.filter(ToDo.status == status)

    todos = session.scalars(query.offset(offset).limit(limit)).all()

    return {'todos': todos}


@router.delete('/{todo_id}', response_model=Message)
def delete_todo(todo_id: int, session: T_Session, user: T_CurrentUser):
    todo = session.scalar(
        select(ToDo).where(ToDo.user_id == user.id, ToDo.id == todo_id)
    )

    if not todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    session.delete(todo)
    session.commit()

    return {'message': 'Task has been deleted successfully.'}


@router.patch('/{todo_id}', response_model=ToDoUpdate)
def patch_todo(
    todo_id: int, session: T_Session, user: T_CurrentUser, todo: ToDoUpdate
):
    db_todo = session.scalar(
        select(ToDo).where(ToDo.user_id == user.id, ToDo.id == todo_id)
    )

    if not db_todo:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Task not found.'
        )

    for key, value in todo.model_dump(exclude_unset=True).items():
        setattr(db_todo, key, value)

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)

    return db_todo
