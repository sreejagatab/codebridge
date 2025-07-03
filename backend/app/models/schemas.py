"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
from enum import Enum


class ProjectStatus(str, Enum):
    discovered = "discovered"
    analyzed = "analyzed"
    processed = "processed"
    published = "published"
    archived = "archived"


class ContentStatus(str, Enum):
    draft = "draft"
    enhanced = "enhanced"
    published = "published"
    archived = "archived"


class ProjectBase(BaseModel):
    platform: str = Field(..., min_length=1, max_length=50, description="Platform name (github, huggingface, etc.)")
    url: str = Field(..., description="Repository or project URL")
    name: str = Field(..., min_length=1, max_length=255, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    stars: Optional[int] = Field(0, ge=0, description="Number of stars/likes")
    language: Optional[str] = Field(None, max_length=50, description="Primary programming language")
    topics: Optional[List[str]] = Field(default_factory=list, description="Project topics/tags")
    quality_score: Optional[float] = Field(None, ge=0.0, le=10.0, description="Quality score (0-10)")
    status: ProjectStatus = Field(ProjectStatus.discovered, description="Project processing status")

    @validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

    @validator('platform')
    def validate_platform(cls, v):
        allowed_platforms = ['github', 'huggingface', 'gitlab', 'kaggle', 'bitbucket']
        if v.lower() not in allowed_platforms:
            raise ValueError(f'Platform must be one of: {", ".join(allowed_platforms)}')
        return v.lower()


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    platform: Optional[str] = Field(None, min_length=1, max_length=50)
    url: Optional[str] = None
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    stars: Optional[int] = Field(None, ge=0)
    language: Optional[str] = Field(None, max_length=50)
    topics: Optional[List[str]] = None
    quality_score: Optional[float] = Field(None, ge=0.0, le=10.0)
    status: Optional[ProjectStatus] = None


class Project(ProjectBase):
    id: int
    scraped_at: datetime
    
    class Config:
        from_attributes = True


class ContentBase(BaseModel):
    project_id: int = Field(..., description="Associated project ID")
    content_type: str = Field(..., min_length=1, max_length=50, description="Type of content (blog, article, etc.)")
    title: str = Field(..., min_length=1, max_length=255, description="Content title")
    slug: str = Field(..., min_length=1, max_length=255, description="URL-friendly slug")
    raw_content: str = Field(..., min_length=1, description="Original content")
    enhanced_content: Optional[str] = Field(None, description="AI-enhanced content")
    meta_description: Optional[str] = Field(None, max_length=160, description="SEO meta description")
    tags: Optional[List[str]] = Field(default_factory=list, description="Content tags")
    status: ContentStatus = Field(ContentStatus.draft, description="Content status")

    @validator('slug')
    def validate_slug(cls, v):
        import re
        if not re.match(r'^[a-z0-9-]+$', v):
            raise ValueError('Slug must contain only lowercase letters, numbers, and hyphens')
        return v

    @validator('content_type')
    def validate_content_type(cls, v):
        allowed_types = ['blog', 'article', 'tutorial', 'guide', 'review']
        if v.lower() not in allowed_types:
            raise ValueError(f'Content type must be one of: {", ".join(allowed_types)}')
        return v.lower()


class ContentCreate(ContentBase):
    pass


class ContentUpdate(BaseModel):
    project_id: Optional[int] = None
    content_type: Optional[str] = Field(None, min_length=1, max_length=50)
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, min_length=1, max_length=255)
    raw_content: Optional[str] = Field(None, min_length=1)
    enhanced_content: Optional[str] = None
    meta_description: Optional[str] = Field(None, max_length=160)
    tags: Optional[List[str]] = None
    status: Optional[ContentStatus] = None


class Content(ContentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# API Response Models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]
    total: int
    page: int
    per_page: int
    pages: int


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str
    database: Optional[dict] = None
    system: Optional[dict] = None


# Authentication Models
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenData(BaseModel):
    username: Optional[str] = None
    permissions: List[str] = []


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., description="User email address")
    is_active: bool = True


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="User password")


class User(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
