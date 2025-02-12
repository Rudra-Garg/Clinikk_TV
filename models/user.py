"""
SQLAlchemy models for user management.

This module defines the User model for storing user information.
"""

import uuid
from sqlalchemy import Column, String, Boolean
from utils.database import Base
from utils.guid import GUID  


class User(Base):
    """
    SQLAlchemy model for a user.
    """
    __tablename__ = "users"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True) 