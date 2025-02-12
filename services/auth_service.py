"""
Authentication service module.

This module defines the AuthService class for handling user registration,
authentication, and retrieval.
"""

import logging
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate
from utils.password import get_password_hash, verify_password

logger = logging.getLogger(__name__)


class AuthService:
    @staticmethod
    def get_user_by_email(db: Session, email: str):
        """
        Retrieve a user by email.

        Args:
            db (Session): Database session.
            email (str): User's email.

        Returns:
            User: The user instance if found, otherwise None.
        """
        logger.debug("Looking up user with email: %s", email)
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        """
        Create a new user with hashed password.

        Args:
            db (Session): Database session.
            user (UserCreate): User creation data.

        Returns:
            User: The created user instance.
        """
        logger.info("Creating user with email: %s", user.email)
        hashed_password = get_password_hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info("User created with id: %s", db_user.id)
        return db_user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        """
        Authenticate a user by verifying email and password.

        Args:
            db (Session): Database session.
            email (str): User's email.
            password (str): Plain text password.

        Returns:
            User: The authenticated user if credentials are valid, otherwise False.
        """
        logger.info("Authenticating user with email: %s", email)
        user = AuthService.get_user_by_email(db, email)
        if not user:
            logger.warning("Authentication failed: user with email %s not found.", email)
            return False
        if not verify_password(password, user.hashed_password):
            logger.warning("Authentication failed: incorrect password for user %s.", email)
            return False
        logger.info("User %s authenticated successfully.", email)
        return user
