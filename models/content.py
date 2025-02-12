"""
SQLAlchemy models for content management.

This module defines the models for storing content records.
"""

import enum
import uuid
from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
from utils.database import Base
from utils.guid import GUID  # Use our custom GUID type


class ContentType(str, enum.Enum):
    """
    Enumeration of content types.
    """
    VIDEO = "video"
    AUDIO = "audio"


class Content(Base):
    """
    SQLAlchemy model for content records.
    """
    __tablename__ = "contents"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content_type = Column(Enum(ContentType), nullable=False)
    storage_url = Column(String)
    thumbnail_url = Column(String, nullable=True)
    duration = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
   