"""Initial migration - create projects and content tables

Revision ID: 001
Revises: 
Create Date: 2025-07-03 07:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create projects table
    op.create_table('projects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('platform', sa.String(length=50), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('stars', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=50), nullable=True),
        sa.Column('topics', sa.Text(), nullable=True),  # JSON string for SQLite
        sa.Column('quality_score', sa.DECIMAL(precision=3, scale=2), nullable=True),
        sa.Column('scraped_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('status', sa.String(length=20), server_default='discovered', nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for projects table
    op.create_index(op.f('ix_projects_id'), 'projects', ['id'], unique=False)
    op.create_index(op.f('ix_projects_platform'), 'projects', ['platform'], unique=False)
    op.create_index(op.f('ix_projects_url'), 'projects', ['url'], unique=True)
    op.create_index(op.f('ix_projects_name'), 'projects', ['name'], unique=False)
    op.create_index(op.f('ix_projects_language'), 'projects', ['language'], unique=False)
    op.create_index(op.f('ix_projects_status'), 'projects', ['status'], unique=False)
    
    # Create content table
    op.create_table('content',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('content_type', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('raw_content', sa.Text(), nullable=False),
        sa.Column('enhanced_content', sa.Text(), nullable=True),
        sa.Column('meta_description', sa.String(length=160), nullable=True),
        sa.Column('tags', sa.Text(), nullable=True),  # JSON string for SQLite
        sa.Column('status', sa.String(length=20), server_default='draft', nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes for content table
    op.create_index(op.f('ix_content_id'), 'content', ['id'], unique=False)
    op.create_index(op.f('ix_content_project_id'), 'content', ['project_id'], unique=False)
    op.create_index(op.f('ix_content_content_type'), 'content', ['content_type'], unique=False)
    op.create_index(op.f('ix_content_slug'), 'content', ['slug'], unique=True)
    op.create_index(op.f('ix_content_status'), 'content', ['status'], unique=False)


def downgrade() -> None:
    # Drop content table
    op.drop_index(op.f('ix_content_status'), table_name='content')
    op.drop_index(op.f('ix_content_slug'), table_name='content')
    op.drop_index(op.f('ix_content_content_type'), table_name='content')
    op.drop_index(op.f('ix_content_project_id'), table_name='content')
    op.drop_index(op.f('ix_content_id'), table_name='content')
    op.drop_table('content')
    
    # Drop projects table
    op.drop_index(op.f('ix_projects_status'), table_name='projects')
    op.drop_index(op.f('ix_projects_language'), table_name='projects')
    op.drop_index(op.f('ix_projects_name'), table_name='projects')
    op.drop_index(op.f('ix_projects_url'), table_name='projects')
    op.drop_index(op.f('ix_projects_platform'), table_name='projects')
    op.drop_index(op.f('ix_projects_id'), table_name='projects')
    op.drop_table('projects')
