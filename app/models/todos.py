from enum import Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from . import table_registry


class ToDoStatus(str, Enum):
    draft = 'draft'
    todo = 'todo'
    doing = 'doing'
    completed = 'completed'
    trash = 'trash'


@table_registry.mapped_as_dataclass
class ToDo:
    __tablename__ = 'todos'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[ToDoStatus]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
