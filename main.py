"""
Main module for the Clinikk TV Backend application.

This module initializes the FastAPI application, configures middleware,
creates database tables, includes API routers, and defines health check endpoints.
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

from routes import content_router, auth_router
from services import StorageService
from utils import engine, Base, get_db, setup_logging

# Setup custom logging for the entire app
setup_logging()
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Clinikk TV Backend",
    description="Backend service for Clinikk TV media streaming platform",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(content_router)
app.include_router(auth_router)


@app.get("/health", summary="Health Check")
async def health_check():
    """
    Health check endpoint.

    Returns a simple status message confirming that the service is running.
    """
    logger.info("Health check endpoint called.")
    return {"status": "healthy"}


@app.get("/health/detailed", summary="Detailed Health Check")
async def detailed_health_check():
    """
    Detailed health check endpoint.

    Checks database and S3 connectivity, returning status for both components.
    """
    logger.info("Detailed health check endpoint called.")
    
    # Check database connectivity
    database_status = "ok"
    try:
        db = next(get_db())
        db.execute(text("SELECT 1"))
        logger.debug("Database connectivity check passed.")
    except SQLAlchemyError as e:
        database_status = f"error: {str(e)}"
        logger.error("Database connectivity error: %s", e)

    # Check S3 connectivity
    try:
        s3_client = StorageService.get_s3_client()
        s3_client.list_buckets()
        s3_status = "ok"
        logger.debug("S3 connectivity check passed.")
    except Exception as e:
        s3_status = f"error: {str(e)}"
        logger.error("S3 connectivity error: %s", e)

    return {"database": database_status, "s3": s3_status}
