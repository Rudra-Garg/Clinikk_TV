"""
Storage service module.

This module provides methods for interacting with AWS S3 storage,
including file uploads, deletion, and generating presigned URLs for streaming.
"""

import logging
from typing import Optional
from urllib.parse import urlparse

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from fastapi import UploadFile
from starlette.concurrency import run_in_threadpool

from config import settings

logger = logging.getLogger(__name__)


class S3UploadException(Exception):
    """
    Custom exception for S3 upload failures.
    """
    pass


class StorageService:
    """
    Service for interacting with S3 storage.
    """

    @staticmethod
    def get_s3_client():
        """
        Create and return a new S3 client.

        Returns:
            boto3.client: An S3 client instance.
        """
        logger.debug("Creating new S3 client.")
        return boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION,
            config=Config(signature_version='s3v4')
        )

    @staticmethod
    async def upload_file(file: UploadFile, content_type: str, content_id: str) -> str:
        """
        Upload a file to S3 storage asynchronously.

        Args:
            file (UploadFile): The file to be uploaded.
            content_type: The type of content (video/audio).
            content_id: The UUID for the content, used as the file name.

        Returns:
            str: The URL of the uploaded file.

        Raises:
            S3UploadException: If the file upload fails.
        """
        # Use the enum's underlying value if available.
        ct = content_type.value if hasattr(content_type, 'value') else str(content_type)
        file_extension = file.filename.split('.')[-1]
        unique_filename = f"{ct}/{str(content_id)}.{file_extension}"
        try:
            logger.info("Initiating file upload for %s to bucket %s", file.filename, settings.STORAGE_BUCKET)
            s3_client = StorageService.get_s3_client()
            # Run the blocking upload in a thread pool
            await run_in_threadpool(
                s3_client.upload_fileobj,
                file.file,
                settings.STORAGE_BUCKET,
                unique_filename,
                ExtraArgs={"ContentType": file.content_type},
            )
            logger.info("File %s uploaded successfully as %s", file.filename, unique_filename)
            # Return the complete S3 URL
            return f"https://{settings.STORAGE_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{unique_filename}"
        except ClientError as e:
            logger.error("Failed to upload file %s due to ClientError: %s", file.filename, e)
            raise S3UploadException(f"Failed to upload file due to S3 ClientError: {str(e)}")
        except Exception as e:
            logger.error("Failed to upload file %s. Error: %s", file.filename, e)
            raise S3UploadException(f"Failed to upload file: {str(e)}")

    @staticmethod
    def generate_presigned_url(storage_url: str, expiration: int = 3600) -> Optional[str]:
        """
        Generate a presigned URL to share an S3 object.

        Args:
            storage_url (str): The URL of the stored object.
            expiration (int): Time in seconds for the presigned URL to remain valid.

        Returns:
            Optional[str]: The presigned URL as a string, or None if generation fails.
        """
        parsed_url = urlparse(storage_url)
        key = parsed_url.path.lstrip('/')
        s3_client = StorageService.get_s3_client()
        try:
            logger.info("Generating presigned URL for key: %s", key)
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.STORAGE_BUCKET, 'Key': key},
                ExpiresIn=expiration
            )
            logger.info("Presigned URL generated successfully for key: %s", key)
        except ClientError as e:
            logger.error("Error generating presigned URL for key %s: %s", key, e)
            return None

        return presigned_url

    @staticmethod
    def delete_file(file_url: str) -> None:
        """
        Delete a file from S3 storage using its URL.

        Args:
            file_url (str): The URL of the file to delete.

        Raises:
            S3UploadException: If deletion fails.
        """
        parsed_url = urlparse(file_url)
        key = parsed_url.path.lstrip('/')
        try:
            s3_client = StorageService.get_s3_client()
            s3_client.delete_object(Bucket=settings.STORAGE_BUCKET, Key=key)
            logger.info("Successfully deleted S3 object with key: %s", key)
        except ClientError as e:
            logger.error("Failed to delete S3 object: %s", e)
            raise S3UploadException(f"Failed to delete S3 object: {str(e)}")
        except Exception as e:
            logger.error("Failed to delete S3 object: %s", e)
            raise S3UploadException(f"Failed to delete S3 object: {str(e)}") 