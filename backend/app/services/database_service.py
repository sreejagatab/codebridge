"""
Database service functions for CRUD operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from typing import List, Optional, Dict, Any
import logging

from app.models.database import Project, Content
from app.models.schemas import ProjectCreate, ProjectUpdate, ContentCreate, ContentUpdate
from app.core.database import get_db

logger = logging.getLogger(__name__)


# Project CRUD operations
def create_project(db: Session, project: ProjectCreate) -> Project:
    """Create a new project"""
    try:
        # Convert to dict and handle topics
        project_data = project.dict()
        if 'topics' in project_data and isinstance(project_data['topics'], list):
            topics_list = project_data.pop('topics')
            db_project = Project(**project_data)
            db_project.topics_list = topics_list
        else:
            db_project = Project(**project_data)
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Created project: {db_project.name} (ID: {db_project.id})")
        return db_project
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating project: {e}")
        raise


def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a project by ID"""
    try:
        return db.query(Project).filter(Project.id == project_id).first()
    except Exception as e:
        logger.error(f"Error getting project {project_id}: {e}")
        raise


def get_project_by_url(db: Session, url: str) -> Optional[Project]:
    """Get a project by URL"""
    try:
        return db.query(Project).filter(Project.url == url).first()
    except Exception as e:
        logger.error(f"Error getting project by URL {url}: {e}")
        raise


def get_projects(db: Session, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None) -> List[Project]:
    """Get projects with optional filtering"""
    try:
        query = db.query(Project)
        
        if filters:
            if 'platform' in filters:
                query = query.filter(Project.platform == filters['platform'])
            if 'status' in filters:
                query = query.filter(Project.status == filters['status'])
            if 'language' in filters:
                query = query.filter(Project.language == filters['language'])
        
        return query.offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting projects: {e}")
        raise


def update_project(db: Session, project_id: int, project_update: ProjectUpdate) -> Optional[Project]:
    """Update a project"""
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        
        update_data = project_update.dict(exclude_unset=True)
        
        # Handle topics update
        if 'topics' in update_data:
            topics_list = update_data.pop('topics')
            db_project.topics_list = topics_list
        
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        db.commit()
        db.refresh(db_project)
        logger.info(f"Updated project: {db_project.name} (ID: {project_id})")
        return db_project
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating project {project_id}: {e}")
        raise


def delete_project(db: Session, project_id: int) -> bool:
    """Delete a project"""
    try:
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return False
        
        # Delete associated content first
        db.query(Content).filter(Content.project_id == project_id).delete()
        
        db.delete(db_project)
        db.commit()
        logger.info(f"Deleted project ID: {project_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting project {project_id}: {e}")
        raise


# Content CRUD operations
def create_content(db: Session, content: ContentCreate) -> Content:
    """Create new content"""
    try:
        content_data = content.dict()
        if 'tags' in content_data and isinstance(content_data['tags'], list):
            tags_list = content_data.pop('tags')
            db_content = Content(**content_data)
            db_content.tags_list = tags_list
        else:
            db_content = Content(**content_data)
        
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        logger.info(f"Created content: {db_content.title} (ID: {db_content.id})")
        return db_content
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating content: {e}")
        raise


def get_content(db: Session, content_id: int) -> Optional[Content]:
    """Get content by ID"""
    try:
        return db.query(Content).filter(Content.id == content_id).first()
    except Exception as e:
        logger.error(f"Error getting content {content_id}: {e}")
        raise


def get_content_by_slug(db: Session, slug: str) -> Optional[Content]:
    """Get content by slug"""
    try:
        return db.query(Content).filter(Content.slug == slug).first()
    except Exception as e:
        logger.error(f"Error getting content by slug {slug}: {e}")
        raise


def get_content_list(db: Session, skip: int = 0, limit: int = 100, filters: Dict[str, Any] = None) -> List[Content]:
    """Get content with optional filtering"""
    try:
        query = db.query(Content)
        
        if filters:
            if 'project_id' in filters:
                query = query.filter(Content.project_id == filters['project_id'])
            if 'content_type' in filters:
                query = query.filter(Content.content_type == filters['content_type'])
            if 'status' in filters:
                query = query.filter(Content.status == filters['status'])
        
        return query.offset(skip).limit(limit).all()
    except Exception as e:
        logger.error(f"Error getting content list: {e}")
        raise


def update_content(db: Session, content_id: int, content_update: ContentUpdate) -> Optional[Content]:
    """Update content"""
    try:
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if not db_content:
            return None
        
        update_data = content_update.dict(exclude_unset=True)
        
        # Handle tags update
        if 'tags' in update_data:
            tags_list = update_data.pop('tags')
            db_content.tags_list = tags_list
        
        for field, value in update_data.items():
            setattr(db_content, field, value)
        
        db.commit()
        db.refresh(db_content)
        logger.info(f"Updated content: {db_content.title} (ID: {content_id})")
        return db_content
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating content {content_id}: {e}")
        raise


def delete_content(db: Session, content_id: int) -> bool:
    """Delete content"""
    try:
        db_content = db.query(Content).filter(Content.id == content_id).first()
        if not db_content:
            return False
        
        db.delete(db_content)
        db.commit()
        logger.info(f"Deleted content ID: {content_id}")
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting content {content_id}: {e}")
        raise


def seed_database(db: Session):
    """
    Seed the database with initial data for testing
    """
    logger.info("Seeding database with initial data...")
    
    # Sample projects
    sample_projects = [
        {
            "platform": "github",
            "url": "https://github.com/microsoft/vscode",
            "name": "Visual Studio Code",
            "description": "Visual Studio Code is a lightweight but powerful source code editor",
            "stars": 150000,
            "language": "TypeScript",
            "topics": ["editor", "typescript", "javascript", "cross-platform"],
            "quality_score": 9.5,
            "status": "analyzed"
        },
        {
            "platform": "github", 
            "url": "https://github.com/fastapi/fastapi",
            "name": "FastAPI",
            "description": "FastAPI framework, high performance, easy to learn, fast to code, ready for production",
            "stars": 65000,
            "language": "Python",
            "topics": ["fastapi", "python", "api", "async"],
            "quality_score": 9.2,
            "status": "discovered"
        },
        {
            "platform": "huggingface",
            "url": "https://huggingface.co/microsoft/DialoGPT-medium",
            "name": "DialoGPT Medium",
            "description": "Large-scale pretrained dialogue response generation model",
            "stars": 500,
            "language": "Python",
            "topics": ["nlp", "dialogue", "gpt", "chatbot"],
            "quality_score": 8.7,
            "status": "discovered"
        }
    ]
    
    # Create projects
    created_projects = []
    for project_data in sample_projects:
        # Check if project already exists
        existing = ProjectService.get_project_by_url(db, project_data["url"])
        if not existing:
            project = ProjectService.create_project(db, project_data)
            created_projects.append(project)
        else:
            created_projects.append(existing)
    
    # Sample content
    sample_contents = [
        {
            "project_id": created_projects[0].id,
            "content_type": "blog_post",
            "title": "Visual Studio Code: The Developer's Best Friend",
            "slug": "vscode-developers-best-friend",
            "raw_content": "# Visual Studio Code\n\nVS Code is a powerful editor...",
            "enhanced_content": "# Visual Studio Code: The Developer's Best Friend\n\nDiscover why VS Code has become...",
            "meta_description": "Explore Visual Studio Code, the lightweight yet powerful editor that's revolutionizing development.",
            "tags": ["vscode", "editor", "development", "productivity"],
            "status": "published"
        },
        {
            "project_id": created_projects[1].id,
            "content_type": "tutorial",
            "title": "Getting Started with FastAPI",
            "slug": "getting-started-fastapi",
            "raw_content": "# FastAPI Tutorial\n\nFastAPI is a modern web framework...",
            "enhanced_content": None,
            "meta_description": "Learn how to build modern APIs with FastAPI framework.",
            "tags": ["fastapi", "python", "api", "tutorial"],
            "status": "draft"
        }
    ]
    
    # Create content
    for content_data in sample_contents:
        # Check if content already exists
        existing = ContentService.get_content_by_slug(db, content_data["slug"])
        if not existing:
            ContentService.create_content(db, content_data)
    
    logger.info("Database seeding completed successfully!")


# Health check functions
def get_database_stats(db: Session) -> Dict[str, Any]:
    """Get database statistics for health checks"""
    try:
        project_count = db.query(Project).count()
        content_count = db.query(Content).count()
        
        # Get counts by status
        project_statuses = db.query(
            Project.status,
            db.func.count(Project.id).label('count')
        ).group_by(Project.status).all()
        
        content_statuses = db.query(
            Content.status,
            db.func.count(Content.id).label('count')
        ).group_by(Content.status).all()
        
        return {
            "total_projects": project_count,
            "total_content": content_count,
            "project_statuses": {status: count for status, count in project_statuses},
            "content_statuses": {status: count for status, count in content_statuses},
        }
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {"error": str(e)}
