"""
Database models for CodeBridge platform
Based on the schema defined in you.md Step 2
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, DECIMAL, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import json

Base = declarative_base()


class Project(Base):
    """
    Core table for content management - projects from various platforms
    Maps to: CREATE TABLE projects in you.md
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(50), nullable=False, index=True)
    url = Column(Text, unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    stars = Column(Integer, default=0)
    language = Column(String(50), index=True)
    topics = Column(Text, default="[]")  # JSON string for SQLite compatibility
    quality_score = Column(DECIMAL(3, 2))
    scraped_at = Column(DateTime, default=func.now())
    status = Column(String(20), default='discovered', index=True)
    
    # Relationships
    content_items = relationship("Content", back_populates="project", cascade="all, delete-orphan")
    
    @property
    def topics_list(self):
        """Convert topics JSON string to list"""
        try:
            return json.loads(self.topics) if self.topics else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @topics_list.setter
    def topics_list(self, value):
        """Convert topics list to JSON string"""
        self.topics = json.dumps(value if value else [])
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', platform='{self.platform}')>"


class Content(Base):
    """
    Content generated from projects
    Maps to: CREATE TABLE content in you.md
    """
    __tablename__ = "content"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    content_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    raw_content = Column(Text, nullable=False)
    enhanced_content = Column(Text)
    meta_description = Column(String(160))
    tags = Column(Text, default="[]")  # JSON string for SQLite compatibility
    status = Column(String(20), default='draft', index=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="content_items")
    
    @property
    def tags_list(self):
        """Convert tags JSON string to list"""
        try:
            return json.loads(self.tags) if self.tags else []
        except (json.JSONDecodeError, TypeError):
            return []
    
    @tags_list.setter
    def tags_list(self, value):
        """Convert tags list to JSON string"""
        self.tags = json.dumps(value if value else [])
    
    def __repr__(self):
        return f"<Content(id={self.id}, title='{self.title}', status='{self.status}')>"


# Export all models for easy importing
__all__ = ["Base", "Project", "Content"]
