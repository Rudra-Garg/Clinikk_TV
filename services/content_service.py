"""
Service layer for content operations.

This module provides the ContentService class with methods for validating file types,
creating, retrieving, updating, and deleting content records in the database.
"""

from fastapi import UploadFile
from sqlalchemy.orm import Session

# Import ContentCreate from the schemas package.
from schemas import ContentCreate


class ContentService:
    @staticmethod
    def validate_file_type(file: UploadFile, content_type: str) -> bool:
        """
        Validate the file type based on content type.

        Args:
            file (UploadFile): The uploaded file.
            content_type (str): The expected content type (e.g., 'video' or 'audio').

        Returns:
            bool: True if the file type is allowed, False otherwise.
        """
        allowed_video_types = ["video/mp4", "video/mpeg"]
        allowed_audio_types = ["audio/mpeg", "audio/mp3", "audio/wav"]

        if content_type == "video":
            return file.content_type in allowed_video_types
        elif content_type == "audio":
            return file.content_type in allowed_audio_types
        return False

    @staticmethod
    def create_content(db: Session, content: ContentCreate, content_id, storage_url: str):
        """
        Create a new content record in the database.

        Args:
            db (Session): Database session.
            content (ContentCreate): Content data.
            content_id: Unique identifier for the content.
            storage_url (str): URL of the uploaded file.

        Returns:
            Content: The created content record.
        """
        from models.content import Content
        db_content = Content(id=content_id, **content.model_dump(), storage_url=storage_url)
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content

    @staticmethod
    def get_content(db: Session, content_id):
        """
        Retrieve a content record by ID.

        Args:
            db (Session): Database session.
            content_id: Unique identifier of the content.

        Returns:
            Content: The content record if found, else None.
        """
        from models.content import Content
        return db.query(Content).filter(Content.id == content_id).first()

    @staticmethod
    def get_contents(db: Session, skip: int = 0, limit: int = 100):
        """
        Retrieve a list of content records with pagination.

        Args:
            db (Session): Database session.
            skip (int): Number of records to skip.
            limit (int): Maximum number of records to return.

        Returns:
            List[Content]: List of content records.
        """
        from models.content import Content
        return db.query(Content).offset(skip).limit(limit).all()

    @staticmethod
    def update_content(db: Session, db_content, update_data: dict):
        """
        Update an existing content record with new data.

        Args:
            db (Session): Database session.
            db_content (Content): The existing content record.
            update_data (dict): Dictionary of fields to update.

        Returns:
            Content: The updated content record.
        """
        for key, value in update_data.items():
            setattr(db_content, key, value)
        db.commit()
        db.refresh(db_content)
        return db_content

    @staticmethod
    def delete_content(db: Session, db_content):
        """
        Delete a content record from the database.

        Args:
            db (Session): Database session.
            db_content (Content): The content record to delete.
        """
        db.delete(db_content)
        db.commit()
