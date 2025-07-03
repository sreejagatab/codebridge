"""
Project API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..core.database import get_db
from ..core.auth import get_current_active_user, require_permissions, get_current_user_optional
from ..models.schemas import (
    Project, ProjectCreate, ProjectUpdate, 
    APIResponse, PaginatedResponse, TokenData
)
from ..services.database_service import (
    create_project, get_project, get_projects, 
    update_project, delete_project, get_project_by_url
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=PaginatedResponse)
async def list_projects(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    platform: Optional[str] = Query(None, description="Filter by platform"),
    status: Optional[str] = Query(None, description="Filter by status"),
    language: Optional[str] = Query(None, description="Filter by programming language"),
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    List discovered projects with optional filtering and pagination.
    
    This endpoint supports optional authentication - authenticated users may see additional data.
    """
    try:
        # Get projects with filters
        filters = {}
        if platform:
            filters['platform'] = platform.lower()
        if status:
            filters['status'] = status.lower()
        if language:
            filters['language'] = language
            
        projects = get_projects(db, skip=skip, limit=limit, filters=filters)
        total = len(get_projects(db, skip=0, limit=10000, filters=filters))  # TODO: Optimize with count query
        
        # Calculate pagination info
        pages = (total + limit - 1) // limit
        page = (skip // limit) + 1
        
        # Convert to dict for response
        projects_data = [
            {
                "id": p.id,
                "platform": p.platform,
                "url": p.url,
                "name": p.name,
                "description": p.description,
                "stars": p.stars,
                "language": p.language,
                "topics": p.topics,
                "quality_score": p.quality_score,
                "status": p.status,
                "scraped_at": p.scraped_at.isoformat()
            }
            for p in projects
        ]
        
        logger.info(
            f"Listed {len(projects)} projects",
            extra={
                "user": current_user.username if current_user else "anonymous",
                "filters": filters,
                "pagination": {"skip": skip, "limit": limit}
            }
        )
        
        return PaginatedResponse(
            success=True,
            message=f"Retrieved {len(projects)} projects",
            data=projects_data,
            total=total,
            page=page,
            per_page=limit,
            pages=pages
        )
        
    except Exception as e:
        logger.error(f"Error listing projects: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve projects"
        )


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("write"))
):
    """
    Create a new project entry.
    
    Requires authentication and 'write' permission.
    """
    try:
        # Check if project already exists
        existing = get_project_by_url(db, project.url)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Project with URL '{project.url}' already exists"
            )
        
        # Create the project
        new_project = create_project(db, project)
        
        logger.info(
            f"Created new project: {new_project.name}",
            extra={
                "user": current_user.username,
                "project_id": new_project.id,
                "platform": new_project.platform
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Project '{new_project.name}' created successfully",
            data={
                "id": new_project.id,
                "name": new_project.name,
                "platform": new_project.platform,
                "url": new_project.url
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create project"
        )


@router.get("/{project_id}", response_model=APIResponse)
async def get_project_details(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    Get detailed information about a specific project.
    
    Optional authentication - authenticated users may see additional details.
    """
    try:
        project = get_project(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )
        
        project_data = {
            "id": project.id,
            "platform": project.platform,
            "url": project.url,
            "name": project.name,
            "description": project.description,
            "stars": project.stars,
            "language": project.language,
            "topics": project.topics,
            "quality_score": project.quality_score,
            "status": project.status,
            "scraped_at": project.scraped_at.isoformat()
        }
        
        logger.info(
            f"Retrieved project details: {project.name}",
            extra={
                "user": current_user.username if current_user else "anonymous",
                "project_id": project_id
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Project '{project.name}' retrieved successfully",
            data=project_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve project"
        )


@router.put("/{project_id}", response_model=APIResponse)
async def update_project_details(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("write"))
):
    """
    Update project information.
    
    Requires authentication and 'write' permission.
    """
    try:
        project = get_project(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )
        
        # Update the project
        updated_project = update_project(db, project_id, project_update)
        
        logger.info(
            f"Updated project: {updated_project.name}",
            extra={
                "user": current_user.username,
                "project_id": project_id,
                "changes": project_update.dict(exclude_unset=True)
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Project '{updated_project.name}' updated successfully",
            data={
                "id": updated_project.id,
                "name": updated_project.name,
                "status": updated_project.status
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update project"
        )


@router.delete("/{project_id}", response_model=APIResponse)
async def delete_project_record(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(require_permissions("delete"))
):
    """
    Delete a project record.
    
    Requires authentication and 'delete' permission.
    """
    try:
        project = get_project(db, project_id)
        if not project:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Project with ID {project_id} not found"
            )
        
        project_name = project.name
        delete_project(db, project_id)
        
        logger.warning(
            f"Deleted project: {project_name}",
            extra={
                "user": current_user.username,
                "project_id": project_id
            }
        )
        
        return APIResponse(
            success=True,
            message=f"Project '{project_name}' deleted successfully",
            data={"deleted_id": project_id}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting project {project_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete project"
        )
