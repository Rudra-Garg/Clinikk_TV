"""
Schemas for content operations.

This module defines the Pydantic models for content-related operations,
including creation, updating, and representation of content.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from models.content_type import ContentType


class ContentBase(BaseModel):
    """
    Base model for content attributes.
    """
    title: str
    description: str
    content_type: ContentType
    duration: int
    thumbnail_url: Optional[str] = None


class ContentCreate(ContentBase):
    """
    Model for creating new content.
    """
    pass


class ContentUpdate(BaseModel):
    """
    Model for updating existing content.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None
    thumbnail_url: Optional[str] = None


class Content(ContentBase):
    """
    Model representing content with additional metadata.
    """
    id: UUID
    storage_url: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        """
        Pydantic configuration to allow attribute-based initialization.
        """
        from_attributes = True
