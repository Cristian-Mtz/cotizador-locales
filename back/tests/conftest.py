from __future__ import annotations

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from pymongo import MongoClient
from testcontainers.mongodb import MongoDbContainer

@pytest.fixture(scope="session")
def mongo_container() -> Generator[MongoDbContainer, None, None]:
    with MongoDbContainer("mongo:7") as mongo:
        yield mongo

@pytest.fixture(scope="session")
def mongo_uri(mongo_container: MongoDbContainer) -> str:
    return mongo_container.get_connection_url()

@pytest.fixture(scope="session", autouse=True)
def _set_env(mongo_uri: str) -> None:
    os.environ["MONGODB_URI"] = mongo_uri
    os.environ["MONGODB_DB"] = "test_db"
    os.environ["API_V1_PREFIX"] = "/api"
    os.environ["CORS_ORIGINS"] = "http://localhost:4200"
    os.environ["ENVIRONMENT"] = "test"

@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    from app.main import create_app
    app = create_app()
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def mongo_sync(mongo_uri: str):
    cli = MongoClient(mongo_uri)
    db = cli["test_db"]
    yield db
    cli.close()
