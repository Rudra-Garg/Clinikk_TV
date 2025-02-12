"""
Authentication API routes.

This module defines endpoints for user registration and login, returning JWT tokens upon successful authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from utils.database import get_db
from schemas.user import User, UserCreate, Token, UserLogin
from services.auth_service import AuthService
from utils.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)


@router.post("/register", response_model=User, summary="Register a new user", description="Create a new user account")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.

    Checks if the email is already registered and creates a new user record.
    """
    db_user = AuthService.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return AuthService.create_user(db, user)


@router.post("/token", response_model=Token, summary="User login", description="Authenticate a user and return a JWT token")
def login_for_access_token(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and provide access token.

    Verifies user credentials and returns a JWT access token on success.
    """
    user = AuthService.authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
