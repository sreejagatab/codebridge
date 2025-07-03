"""
Health check endpoints
"""

from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import psutil
import platform
import logging

from ..core.config import settings
from ..core.database import get_db, get_connection_info, test_connection
from ..services.database_service import get_database_stats

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Health check endpoint
    Returns application health status and system information
    """
    try:
        # System information
        system_info = {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "hostname": platform.node(),
            "processor": platform.processor(),
        }
        
        # Memory and CPU info
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        performance_info = {
            "cpu_usage_percent": cpu_percent,
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_usage_percent": memory.percent,
        }
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": settings.VERSION,
            "app_name": settings.APP_NAME,
            "environment": "development" if settings.DEBUG else "production",
            "features": {
                "step_1": "✅ Project Skeleton Setup",
                "step_2": "✅ Database Foundation", 
                "step_3": "✅ Basic API Framework",
                "authentication": "✅ JWT Authentication",
                "rate_limiting": "✅ Rate Limiting",
                "api_validation": "✅ Pydantic Validation",
                "api_docs": "✅ OpenAPI/Swagger"
            },
            "endpoints": {
                "auth": "/api/auth/login",
                "projects": "/api/projects",
                "content": "/api/content",
                "docs": "/docs",
                "health_db": "/api/health/database"
            },
            "system": system_info,
            "performance": performance_info,
        }
        
        logger.info("Health check completed successfully", extra={"health_status": "healthy"})
        
        return health_data
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}", exc_info=True)
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "version": settings.VERSION,
            "app_name": settings.APP_NAME,
        }


@router.get("/health/simple", status_code=status.HTTP_200_OK)
async def simple_health_check():
    """
    Simple health check endpoint
    Returns basic status information
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Service is running"
    }


@router.get("/health/database", status_code=status.HTTP_200_OK)
async def database_health_check(db: Session = Depends(get_db)):
    """
    Database health check endpoint
    Returns database connectivity status and statistics
    """
    try:
        # Test database connection
        db_connected = await test_connection()
        
        # Get connection info
        connection_info = get_connection_info()
        
        # Get database statistics if connected
        db_stats = {}
        if db_connected:
            try:
                db_stats = get_database_stats(db)
            except Exception as stats_error:
                logger.warning(f"Could not retrieve database stats: {stats_error}")
                db_stats = {"error": "Stats unavailable"}
        
        health_data = {
            "status": "healthy" if db_connected else "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": {
                "connected": db_connected,
                "connection_info": connection_info,
                "statistics": db_stats
            }
        }
        
        if db_connected:
            logger.info("Database health check completed successfully")
        else:
            logger.error("Database health check failed - no connection")
            
        return health_data
        
    except Exception as e:
        logger.error(f"Database health check error: {str(e)}", exc_info=True)
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "database": {
                "connected": False,
                "error": str(e)
            }
        }
