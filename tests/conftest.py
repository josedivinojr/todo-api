from contextlib import contextmanager
from datetime import datetime

import factory
import pytest
from factory import fuzzy
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from app.app import app
from app.db.database import get_session
from app.models import table_registry
from app.models.todos import ToDo, ToDoStatus
from app.models.users import User
from app.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'username_{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@email.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}_password')


class ToDoFactory(factory.Factory):
    class Meta:
        model = ToDo

    title = factory.Faker('text')
    description = factory.Faker('text')
    status = fuzzy.FuzzyChoice(ToDoStatus)
    user_id = 1


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as test_client:
        app.dependency_overrides[get_session] = get_session_override

        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def session(engine):
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def engine():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        _engine = create_engine(postgres.get_connection_url())

        with _engine.begin():
            yield _engine


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    event.listen(model, 'before_insert', fake_time_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time


@pytest.fixture
def user(session):
    password = '@Password123'
    user = UserFactory(
        password=get_password_hash(password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = password  # Monkey Patch

    return user


@pytest.fixture
def another_user(session):
    another_user = UserFactory()

    session.add(another_user)
    session.commit()
    session.refresh(another_user)

    return another_user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/v1/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    return response.json()['access_token']
