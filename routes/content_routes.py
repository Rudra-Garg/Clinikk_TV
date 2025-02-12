"""
API routes for content operations.

This module defines endpoints for creating, listing, retrieving, updating,
deleting, and streaming content records.
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session

from controllers import ContentController
from models import ContentType, User
# Import models and schemas directly from their packages.
from schemas import Content, ContentCreate, ContentUpdate
from utils import get_db, get_current_user

router = APIRouter(
    tags=["content"],
    responses={404: {"description": "Not found"}},
)


@router.post("/content/", response_model=Content, summary="Create new content",
             description="Uploads a file and creates a content record")
async def create_content(
        title: str = Form(...),
        description: str = Form(...),
        content_type: ContentType = Form(...),
        duration: int = Form(...),
        thumbnail_url: Optional[str] = Form(None),
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Create new content.

    This endpoint handles file uploads and creates a corresponding content record in the database.
    """
    content_data = ContentCreate(
        title=title,
        description=description,
        content_type=content_type,
        duration=duration,
        thumbnail_url=thumbnail_url
    )
    return await ContentController.create_content(db, content_data, file)


@router.get("/content/", response_model=List[Content], summary="List contents",
            description="Retrieve a list of content records")
def list_contents(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """
    List content records with pagination.
    """
    return ContentController.get_contents(db, skip=skip, limit=limit)


@router.get("/content/{content_id}", response_model=Content, summary="Get content",
            description="Retrieve a specific content record by ID")
def get_content(content_id: UUID, db: Session = Depends(get_db)):
    """
    Retrieve a content record by its ID.
    """
    content = ContentController.get_content(db, content_id)
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content


@router.put("/content/{content_id}", response_model=Content, summary="Update content",
            description="Update a content record and optionally upload a new file")
async def update_content(
        content_id: UUID,
        title: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        duration: Optional[int] = Form(None),
        thumbnail_url: Optional[str] = Form(None),
        file: Optional[UploadFile] = File(None),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Update an existing content record.

    Allows updating of content attributes and optionally uploading a new file. 
    """
    content_update = ContentUpdate(
        title=title,
        description=description,
        duration=duration,
        thumbnail_url=thumbnail_url
    )
    return await ContentController.update_content(db, content_id, content_update, file)


@router.delete("/content/{content_id}", summary="Delete content", description="Delete a content record by ID")
def delete_content(
        content_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    """
    Delete a content record.
    """
    return ContentController.delete_content(db, content_id)


@router.get("/content/{content_id}/stream", summary="Stream content",
            description="Generate a presigned URL for streaming content")
def stream_content(content_id: UUID, db: Session = Depends(get_db)):
    """
    Generate a presigned URL and redirect for streaming content.
    """
    presigned_url = ContentController.stream_content(db, content_id)
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=presigned_url)
