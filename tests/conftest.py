from contextlib import contextmanager
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from fastapi_zero.app import app
from fastapi_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def creat_user(client):
    response = client.post(
        '/users/1',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': '456123',
        },
    )
    return response


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)

    engine.dispose()


@contextmanager
def _mock_db_time(*, model, time=datetime(2024, 1, 1)):

    def fake_time_insert_hook(mapper, connection, target):
        if hasattr(target, 'created_at'):
            target.created_at = time

    def fake_time_update_hook(mapper, connection, target):
        if hasattr(target, 'updated_at'):
            target.updated_at = time

    event.listen(model, 'before_insert', fake_time_insert_hook)
    event.listen(model, 'before_update', fake_time_update_hook)

    yield time

    event.remove(model, 'before_insert', fake_time_insert_hook)
    event.remove(model, 'before_update', fake_time_update_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
