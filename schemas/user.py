"""
Schemas for user-related operations.

This module defines the Pydantic models for user creation, login, and token management.
"""

from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """
    Base schema for user attributes.
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str


class User(UserBase):
    """
    Schema representing a user with additional details.
    """
    id: UUID
    is_active: bool
    model_config = {"from_attributes": True}


class Token(BaseModel):
    """
    Schema for JWT token response.
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data.
    """
    email: str | None = None


class UserLogin(BaseModel):
    """
    Schema for user login credentials.
    """
    email: EmailStr
    password: str
