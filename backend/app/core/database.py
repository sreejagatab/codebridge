"""
Database configuration and connection management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
import logging

from .config import settings

logger = logging.getLogger(__name__)

# Synchronous database engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)

# Asynchronous database engine for async operations
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG,
)

# Session factories
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


def get_db() -> Session:
    """
    Dependency for getting database session in FastAPI routes
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    """
    Dependency for getting async database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def create_tables():
    """
    Create all tables in the database
    Used for testing and initial setup
    """
    from app.models.database import Base
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")


def drop_tables():
    """
    Drop all tables in the database
    Used for testing and reset operations
    """
    from app.models.database import Base
    Base.metadata.drop_all(bind=engine)
    logger.info("Database tables dropped successfully")


async def test_connection():
    """
    Test database connectivity
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute("SELECT 1")
            row = result.fetchone()
            if row and row[0] == 1:
                logger.info("✅ Database connection successful")
                return True
            else:
                logger.error("❌ Database connection test failed")
                return False
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
        return False


def get_connection_info():
    """
    Get database connection information for health checks
    """
    try:
        # Parse connection info from URL (safe extraction)
        url_parts = settings.DATABASE_URL.split('@')
        if len(url_parts) > 1:
            host_db = url_parts[1].split('/')
            host = host_db[0].split(':')[0] if ':' in host_db[0] else host_db[0]
            database = host_db[1] if len(host_db) > 1 else 'unknown'
        else:
            host = "unknown"
            database = "unknown"
            
        return {
            "host": host,
            "database": database,
            "pool_size": engine.pool.size(),
            "checked_out_connections": engine.pool.checkedout(),
            "overflow_connections": engine.pool.overflow(),
            "invalid_connections": engine.pool.invalidated(),
        }
    except Exception as e:
        logger.error(f"Error getting connection info: {e}")
        return {
            "host": "error",
            "database": "error",
            "error": str(e)
        }
