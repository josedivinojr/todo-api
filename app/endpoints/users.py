from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.models.users import User
from app.schemas.message import Message
from app.schemas.users import UserList, UserPublic, UserSchema
from app.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 10, offset: int = 0):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: T_Session):
    """Creates User"""
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    existing_username = session.scalar(
        select(User).where(User.username == user.username)
    )
    if existing_username:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Username already exists',
        )

    existing_email = session.scalar(
        select(User).where(User.email == user.email)
    )
    if existing_email:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email already exists',
        )

    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/{user_id}', response_model=UserPublic)
def read_user(user_id: int, session: T_Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )

    current_user.email = user.email
    current_user.username = user.username
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permission'
        )
    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
