"""
This package aggregates all API route modules for the Clinikk TV Backend application.
It includes routes for content operations and user authentication.
"""
from .content_routes import router as content_router
from .auth_routes import router as auth_router

__all__ = ["content_router", "auth_router"]
