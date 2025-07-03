"""
Content API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..core.database import get_db
from ..core.auth import get_current_active_user, require_permissions, get_current_user_optional
from ..models.schemas import (
    Content, ContentCreate, ContentUpdate,
    APIResponse, PaginatedResponse, TokenData
)
from ..services.database_service import (
    create_content, get_content, get_content_list,
    update_content, delete_content, get_content_by_slug,
    get_project  # To validate project exists
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/content", tags=["content"])


@router.get("", response_model=PaginatedResponse)
async def list_content(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    content_type: Optional[str] = Query(None, description="Filter by content type"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    List generated content with optional filtering and pagination.
    
    This endpoint supports optional authentication - authenticated users may see additional data.
    """
    try:
        # Build filters
        filters = {}
        if project_id:
            filters['project_id'] = project_id
        if content_type:
            filters['content_type'] = content_type.lower()
        if status:
            filters['status'] = status.lower()
            
        content_list = get_content_list(db, skip=skip, limit=limit, filters=filters)
        total = len(get_content_list(db, skip=0, limit=10000, filters=filters))  # TODO: Optimize with count query
        
        # Calculate pagination info
        pages = (total + limit - 1) // limit
        page = (skip // limit) + 1
        
        # Convert to dict for response
        content_data = [
            {
                "id": c.id,
                "project_id": c.project_id,
                "content_type": c.content_type,
                "title": c.title,
                "slug": c.slug,
                "meta_description": c.meta_description,
                "tags": c.tags,
                "status": c.status,
                "created_at": c.created_at.isoformat(),
                # Include content lengths instead of full content for list view
                "raw_content_length": len(c.raw_content) if c.raw_content else 0,
                "enhanced_content_length": len(c.enhanced_content) if c.enhanced_content else 0
            }
            for c in content_list
        ]
        
        logger.info(
            f"Listed {len(content_list)} content items",
            extra={
                "user": current_user.username if current_user else "anonymous",
                "filters": filters,
                "pagination": {"skip": skip, "limit": limit}
            }
        )
        
        return PaginatedResponse(
            success=True,
            message=f"Retrieved {len(content_list)} content items",
            data=content_data,
            total=total,
            page=page,
            per_page=limit,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Error listing content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content"
        )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_new_content(
    content: ContentCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("write"))
):
    """
    Create new content entry.
    
    Requires authentication and 'write' permission.
    """
    try:
        # Validate that project exists
        project = get_project(db, content.project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {content.project_id} not found"
            )
        
        # Check if content with this slug already exists
        existing = get_content_by_slug(db, content.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Content with slug '{content.slug}' already exists"
            )
        
        # Create the content
        new_content = create_content(db, content)
        
        logger.info(
            f"Created new content: {new_content.title}",
            extra={
                "user": current_user.username,
                "content_id": new_content.id,
                "project_id": new_content.project_id,
                "content_type": new_content.content_type
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Content '{new_content.title}' created successfully",
            data={
                "id": new_content.id,
                "title": new_content.title,
                "slug": new_content.slug,
                "content_type": new_content.content_type
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating content: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create content"
        )


@router.get("/{content_id}", response_model=APIResponse)
async def get_content_details(
    content_id: int,
    include_raw: bool = Query(False, description="Include raw content in response"),
    include_enhanced: bool = Query(False, description="Include enhanced content in response"),
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    Get detailed information about specific content.
    
    Optional authentication - authenticated users may see additional details.
    Content inclusion is controlled by query parameters to manage response size.
    """
    try:
        content = get_content(db, content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with ID {content_id} not found"
            )
        
        content_data = {
            "id": content.id,
            "project_id": content.project_id,
            "content_type": content.content_type,
            "title": content.title,
            "slug": content.slug,
            "meta_description": content.meta_description,
            "tags": content.tags,
            "status": content.status,
            "created_at": content.created_at.isoformat()
        }
        
        # Include content based on query parameters
        if include_raw and content.raw_content:
            content_data["raw_content"] = content.raw_content
        if include_enhanced and content.enhanced_content:
            content_data["enhanced_content"] = content.enhanced_content
            
        # Always include content lengths
        content_data["raw_content_length"] = len(content.raw_content) if content.raw_content else 0
        content_data["enhanced_content_length"] = len(content.enhanced_content) if content.enhanced_content else 0
        
        logger.info(
            f"Retrieved content details: {content.title}",
            extra={
                "user": current_user.username if current_user else "anonymous",
                "content_id": content_id,
                "include_raw": include_raw,
                "include_enhanced": include_enhanced
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Content '{content.title}' retrieved successfully",
            data=content_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving content {content_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content"
        )


@router.put("/{content_id}", response_model=APIResponse)
async def update_content_details(
    content_id: int,
    content_update: ContentUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("write"))
):
    """
    Update content information.
    
    Requires authentication and 'write' permission.
    """
    try:
        content = get_content(db, content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with ID {content_id} not found"
            )
        
        # If project_id is being updated, validate the new project exists
        if content_update.project_id and content_update.project_id != content.project_id:
            project = get_project(db, content_update.project_id)
            if not project:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Project with ID {content_update.project_id} not found"
                )
        
        # If slug is being updated, check for conflicts
        if content_update.slug and content_update.slug != content.slug:
            existing = get_content_by_slug(db, content_update.slug)
            if existing and existing.id != content_id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Content with slug '{content_update.slug}' already exists"
                )
        
        # Update the content
        updated_content = update_content(db, content_id, content_update)
        
        logger.info(
            f"Updated content: {updated_content.title}",
            extra={
                "user": current_user.username,
                "content_id": content_id,
                "changes": content_update.dict(exclude_unset=True)
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Content '{updated_content.title}' updated successfully",
            data={
                "id": updated_content.id,
                "title": updated_content.title,
                "status": updated_content.status
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating content {content_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update content"
        )


@router.delete("/{content_id}", response_model=APIResponse)
async def delete_content_record(
    content_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("delete"))
):
    """
    Delete a content record.
    
    Requires authentication and 'delete' permission.
    """
    try:
        content = get_content(db, content_id)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with ID {content_id} not found"
            )
        
        content_title = content.title
        delete_content(db, content_id)
        
        logger.warning(
            f"Deleted content: {content_title}",
            extra={
                "user": current_user.username,
                "content_id": content_id
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Content '{content_title}' deleted successfully",
            data={"deleted_id": content_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting content {content_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete content"
        )


@router.get("/by-slug/{slug}", response_model=APIResponse)
async def get_content_by_slug_endpoint(
    slug: str,
    include_raw: bool = Query(False, description="Include raw content in response"),
    include_enhanced: bool = Query(True, description="Include enhanced content in response"),
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    Get content by its URL slug.
    
    This endpoint is useful for public content access and SEO-friendly URLs.
    """
    try:
        content = get_content_by_slug(db, slug)
        if not content:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content with slug '{slug}' not found"
            )
        
        content_data = {
            "id": content.id,
            "project_id": content.project_id,
            "content_type": content.content_type,
            "title": content.title,
            "slug": content.slug,
            "meta_description": content.meta_description,
            "tags": content.tags,
            "status": content.status,
            "created_at": content.created_at.isoformat()
        }
        
        # Include content based on query parameters (enhanced by default for public access)
        if include_raw and content.raw_content:
            content_data["raw_content"] = content.raw_content
        if include_enhanced and content.enhanced_content:
            content_data["enhanced_content"] = content.enhanced_content
            
        logger.info(
            f"Retrieved content by slug: {slug}",
            extra={
                "user": current_user.username if current_user else "anonymous",
                "content_id": content.id,
                "slug": slug
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Content '{content.title}' retrieved successfully",
            data=content_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving content by slug {slug}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve content"
        )
