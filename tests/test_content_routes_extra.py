import io
import uuid

import pytest

from models.user import User
from utils.security import get_current_user


# Override authentication dependency so that content routes that require a logged-in user work during tests.
@pytest.fixture(autouse=True)
def override_get_current_user(client):
    client.app.dependency_overrides[get_current_user] = lambda: User(
        id=uuid.uuid4(), email="testuser@example.com", is_active=True
    )


# Override the storage service methods to bypass actual S3 interactions.
@pytest.fixture(autouse=True)
def override_storage_service(monkeypatch):
    async def dummy_upload_file(file, content_type, content_id):
        return f"http://dummy-url/{content_id}"

    from services.storage_service import StorageService
    monkeypatch.setattr(StorageService, "upload_file", dummy_upload_file)
    monkeypatch.setattr(StorageService, "generate_presigned_url",
                        lambda storage_url, expiration=3600: "http://dummy-presigned-url")


def create_dummy_content(client, title="Dummy Video", description="Dummy description", content_type="video",
                         duration="120"):
    file_content = b"dummy video content" if content_type == "video" else b"dummy audio content"
    # Choose an appropriate file and MIME type based on the content type.
    file_tuple = ("test.mp4", io.BytesIO(file_content), "video/mp4") if content_type == "video" else (
        "test.mp3", io.BytesIO(file_content), "audio/mpeg")
    files = {"file": file_tuple}
    form_data = {
        "title": title,
        "description": description,
        "content_type": content_type,
        "duration": duration
    }
    response = client.post("/content/", data=form_data, files=files)
    assert response.status_code == 200, response.text
    return response.json()


def test_update_content_without_file(client):
    # Create a new content record.
    content = create_dummy_content(client)
    content_id = content["id"]

    update_data = {
        "title": "Updated Title",
        "description": "Updated Description",
        "duration": "150"
    }
    # Update content without providing a file.
    response = client.put(f"/content/{content_id}", data=update_data)
    assert response.status_code == 200, response.text
    updated_content = response.json()
    assert updated_content["title"] == update_data["title"]
    assert updated_content["description"] == update_data["description"]
    assert updated_content["duration"] == int(update_data["duration"])


def test_update_content_with_file(client):
    # Create initial content.
    content = create_dummy_content(client)
    content_id = content["id"]

    update_data = {
        "title": "Updated With File",
        "description": "Updated Description with file",
        "duration": "180"
    }
    # Provide a new file as part of the update.
    file_content = b"updated dummy video content"
    files = {
        "file": ("updated.mp4", io.BytesIO(file_content), "video/mp4")
    }
    response = client.put(f"/content/{content_id}", data=update_data, files=files)
    assert response.status_code == 200, response.text
    updated_content = response.json()
    assert updated_content["title"] == update_data["title"]
    # Check that the dummy storage service returns the expected URL.
    assert "http://dummy-url" in updated_content["storage_url"]


def test_update_content_not_found(client):
    non_existent_id = str(uuid.uuid4())
    update_data = {
        "title": "Non-existent Content"
    }
    response = client.put(f"/content/{non_existent_id}", data=update_data)
    assert response.status_code == 404, response.text


def test_delete_content(client):
    # Create a content record.
    content = create_dummy_content(client)
    content_id = content["id"]

    # Delete the created content.
    response = client.delete(f"/content/{content_id}")
    assert response.status_code == 200, response.text
    msg = response.json()
    assert msg["detail"] == "Content deleted successfully"

    # Verify that the content no longer exists.
    response = client.get(f"/content/{content_id}")
    assert response.status_code == 404, response.text


def test_delete_content_not_found(client):
    non_existent_id = str(uuid.uuid4())
    response = client.delete(f"/content/{non_existent_id}")
    assert response.status_code == 404, response.text


def test_stream_content_success(client):
    # Create a content record.
    content = create_dummy_content(client)
    content_id = content["id"]

    # Request the streaming endpoint.
    response = client.get(f"/content/{content_id}/stream", allow_redirects=False)
    # Expect a redirection response (commonly 302 or 307).
    assert response.status_code in (302, 307), response.text
    location = response.headers.get("location")
    # Since we've overridden generate_presigned_url, verify the expected dummy URL.
    assert location == "http://dummy-presigned-url", response.text


def test_stream_content_not_found(client):
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/content/{non_existent_id}/stream")
    assert response.status_code == 404, response.text
