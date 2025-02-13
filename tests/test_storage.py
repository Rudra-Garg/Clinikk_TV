import pytest
from fastapi import UploadFile
from services.storage_service import StorageService, S3UploadException


class DummyUploadFile:
    filename = "test.mp4"
    content_type = "video/mp4"

    async def read(self):
        return b"fake video content"


@pytest.mark.asyncio
async def test_upload_success(monkeypatch):
    async def dummy_put_object(*args, **kwargs):
        return True

    monkeypatch.setattr(StorageService, 'upload_file', dummy_put_object)
    # This test would need to be adjusted to actually call StorageService.upload_file
    file = DummyUploadFile()
    # Simulate success case testing here.


@pytest.mark.asyncio
async def test_upload_failure(monkeypatch):
    async def dummy_put_object(*args, **kwargs):
        from botocore.exceptions import ClientError
        raise ClientError({"Error": {"Message": "Simulated S3 error"}}, "PutObject")

    monkeypatch.setattr("boto3.client",
                        lambda *args, **kwargs: type("DummyClient", (), {"put_object": dummy_put_object}))
    file = DummyUploadFile()
    with pytest.raises(S3UploadException):
        await StorageService.upload_file(file, "video", "dummy-content-id")
