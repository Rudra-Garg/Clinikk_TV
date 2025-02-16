"""
Controller layer for handling content-related operations.

This module defines the ContentController class which handles validation,
file uploads, retrieval, updates, deletion, and streaming of content.
"""

import logging
import uuid

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from models import Content
from schemas import ContentCreate, ContentUpdate

from services import ContentService, StorageService, S3UploadException

logger = logging.getLogger(__name__)


class ContentController:
    """
    Controller for handling content-related actions.
    """

    @staticmethod
    async def create_content(db: Session, content: ContentCreate, file: UploadFile):
        """
        Create new content.

        Validates the file type, uploads the file to storage,
        and creates a new content record in the database.

        Args:
            db (Session): Database session.
            content (ContentCreate): The content data.
            file (UploadFile): The file to be uploaded.

        Returns:
            Content: The created content record.

        Raises:
            HTTPException: If the file type is invalid or upload fails.
        """
        logger.info("Received request to create content with title: %s", content.title)
        if not ContentService.validate_file_type(file, content.content_type):
            logger.error("Invalid file type for content type: %s", content.content_type)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type for {content.content_type} content"
            )

        # Generate a new UUID to be used as both the content id and file name
        content_id = uuid.uuid4()
        try:
            storage_url = await StorageService.upload_file(file, content.content_type, content_id)
        except S3UploadException as e:
            logger.error("Storage upload failed: %s", e)
            raise HTTPException(status_code=500, detail=str(e))
        logger.debug("File uploaded to storage with URL: %s", storage_url)
        created_content = ContentService.create_content(db, content, content_id, storage_url)
        logger.info("Content created with id: %s", created_content.id)
        return created_content

    @staticmethod
    def get_content(db: Session, content_id):
        """
        Retrieve a single content by its ID.

        Args:
            db (Session): Database session.
            content_id (UUID): The ID of the content.

        Returns:
            Content: The content record if found.
        """
        logger.debug("Fetching content with id: %s", content_id)
        return ContentService.get_content(db, content_id)

    @staticmethod
    def get_contents(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve a list of content records.

        Args:
            db (Session): Database session.
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to return.

        Returns:
            List[Content]: List of content records.
        """
        logger.debug("Listing contents with skip: %d and limit: %d", skip, limit)
        return ContentService.get_contents(db, skip=skip, limit=limit)

    @staticmethod
    async def update_content(db: Session, content_id, content_update: ContentUpdate, file: UploadFile = None):
        """
        Update content metadata only.

        Args:
            db (Session): Database session.
            content_id: ID of the content to update.
            content_update (ContentUpdate): The updated metadata.
            file (UploadFile, optional): If provided, file updates are rejected.

        Returns:
            Updated content record.

        Raises:
            HTTPException: If the content is not found or if a file is provided.
        """
        logger.info("Received request to update content id: %s", content_id)
        db_content = ContentService.get_content(db, content_id)
        if not db_content:
            logger.error("Content with id %s not found for update.", content_id)
            raise HTTPException(status_code=404, detail="Content not found")

        update_data = content_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_content, key, value)

        db.commit()
        db.refresh(db_content)
        logger.info("Content with id %s metadata updated successfully.", content_id)
        return db_content

    @staticmethod
    def delete_content(db: Session, content_id):
        """
        Delete a content record.

        Args:
            db (Session): Database session.
            content_id (UUID): ID of the content to delete.

        Returns:
            dict: A confirmation message.

        Raises:
            HTTPException: If the content is not found.
        """
        logger.info("Received request to delete content id: %s", content_id)
        db_content = ContentService.get_content(db, content_id)
        if not db_content:
            logger.error("Content with id %s not found for deletion.", content_id)
            raise HTTPException(status_code=404, detail="Content not found")
        # Delete the associated S3 object before removing the database record
        StorageService.delete_file(db_content.storage_url)
        ContentService.delete_content(db, db_content)
        logger.info("Content with id %s deleted successfully.", content_id)
        return {"detail": "Content deleted successfully"}

    @staticmethod
    def stream_content(db: Session, content_id):
        """
        Generate a presigned URL for streaming a content file.

        Args:
            db (Session): Database session.
            content_id (UUID): ID of the content to stream.

        Returns:
            str: A presigned URL for streaming.

        Raises:
            HTTPException: If the content is not found or presigned URL generation fails.
        """
        logger.info("Received request to stream content with id: %s", content_id)
        db_content = ContentService.get_content(db, content_id)
        if not db_content:
            logger.error("Content with id %s not found for streaming.", content_id)
            raise HTTPException(status_code=404, detail="Content not found")
        presigned_url = StorageService.generate_presigned_url(db_content.storage_url)
        if presigned_url is None:
            logger.error("Failed to generate presigned URL for content id: %s", content_id)
            raise HTTPException(status_code=500, detail="Unable to generate presigned URL for streaming.")
        logger.info("Streaming content id %s using presigned URL.", content_id)
        return presigned_url
