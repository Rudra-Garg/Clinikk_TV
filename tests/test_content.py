"""
Unit tests for content endpoints.

This module tests content creation, retrieval, listing, update, and deletion operations.
"""

from fastapi.testclient import TestClient
import pytest
from main import app
from models.content import ContentType
import io
import uuid
from models.user import User
from utils.security import get_current_user
from services.storage_service import StorageService

# Dummy async function to bypass actual S3 uploading during tests.
async def dummy_upload_file(file, content_type, content_id):
    return f"http://dummy-url/{content_id}"

# Override the get_current_user dependency so that endpoints protected by authentication work in tests.
@pytest.fixture(autouse=True)
def override_get_current_user(client):
    client.app.dependency_overrides[get_current_user] = lambda: User(
        id=uuid.uuid4(), email="testuser@example.com", is_active=True
    )

# Override the S3 upload function so that file uploads return a dummy URL.
@pytest.fixture(autouse=True)
def override_storage_service(monkeypatch):
    monkeypatch.setattr(StorageService, "upload_file", dummy_upload_file)

def test_create_content(client):
    """
    Test valid content creation with a file upload.
    """
    file_content = b"fake video content"
    files = {
        "file": ("test.mp4", io.BytesIO(file_content), "video/mp4")
    }
    form_data = {
        "title": "Test Video",
        "description": "Test Description",
        "content_type": "video",
        "duration": "120"
    }
    response = client.post("/content/", data=form_data, files=files)
    assert response.status_code == 200, response.text
    content = response.json()
    assert content["title"] == form_data["title"]
    assert content["description"] == form_data["description"]
    # Check that our overridden storage service returns the dummy URL.
    assert "http://dummy-url/" in content.get("storage_url", "")


def test_create_content_invalid_file(client):
    """
    Test content creation with an invalid file type.
    """
    file_content = b"fake document content"
    files = {
        "file": ("test.txt", io.BytesIO(file_content), "text/plain")
    }
    form_data = {
        "title": "Test Document",
        "description": "Invalid file type",
        "content_type": "video",  # Expecting a video file but provided a text file.
        "duration": "60"
    }
    response = client.post("/content/", data=form_data, files=files)
    # An invalid file type should result in a 400 error.
    assert response.status_code == 400, response.text


def test_get_content(client):
    """
    Test retrieval of a specific content record.
    """
    random_uuid = str(uuid.uuid4())
    response = client.get(f"/content/{random_uuid}")
    # Since no content with this UUID exists, we expect a 404 response.
    assert response.status_code == 404


def test_list_contents(client):
    """
    Test retrieval of content list.
    """
    response = client.get("/content/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)