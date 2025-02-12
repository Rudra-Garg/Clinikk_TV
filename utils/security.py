"""
Security utility functions.

This module provides functions for creating JWT access tokens and retrieving the current authenticated user.
"""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import settings
from schemas.user import TokenData
from services.auth_service import AuthService
from utils.database import get_db

bearer_scheme = HTTPBearer()


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): A dictionary containing user information.

    Returns:
        str: Encoded JWT token.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
                           db: Session = Depends(get_db)):
    """
    Retrieve the current authenticated user.

    Args:
        credentials (HTTPAuthorizationCredentials): The Bearer token credentials.
        db (Session): Database session.

    Returns:
        User: The authenticated user.

    Raises:
        HTTPException: If credentials are invalid or user is not found.
    """
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = AuthService.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
