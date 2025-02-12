"""
Test configuration module.

This module provides fixtures for setting up the TestClient and a test database using SQLite.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
# Import Base and get_db from the utils package.
from utils import Base, get_db

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    """
    Fixture to create and yield a test database session.
    """
    Base.metadata.create_all(bind=engine)
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    """
    Fixture to provide a TestClient with dependency override for the database.
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
