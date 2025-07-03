"""
FastAPI Application Main Entry Point
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import json
import time
from datetime import datetime

from .core.config import settings
from .core.logging_config import setup_logging
from .core.auth import check_rate_limit, rate_limiter
from .api.health import router as health_router
from .api.projects import router as projects_router
from .api.content import router as content_router
from .api.auth import router as auth_router

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="CodeBridge API",
    description="""
    🌉 **CodeBridge API** - README-to-Blog Automation Platform
    
    A modern FastAPI application for transforming README files into engaging blog posts.
    
    ## Features
    
    * **Project Management**: Discover and manage code repositories
    * **Content Generation**: Transform README files into blog content
    * **Authentication**: JWT-based secure API access
    * **Rate Limiting**: Built-in request throttling
    * **Real-time Health Monitoring**: System status and metrics
    
    ## Authentication
    
    Most endpoints require authentication. Use the `/auth/login` endpoint to get an access token.
    
    **Demo Credentials:**
    - Username: `admin`, Password: `admin123` (full access)
    - Username: `user`, Password: `user123` (read/write access)
    
    ## Rate Limiting
    
    - **Standard endpoints**: 60 requests per minute
    - **Authenticated endpoints**: Higher limits based on user tier
    
    """,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else "/docs",  # Always show docs for now
    redoc_url="/redoc" if settings.DEBUG else "/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting middleware
@app.middleware("http")
async def rate_limiting_middleware(request: Request, call_next):
    """Apply rate limiting to all requests"""
    try:
        # Skip rate limiting for health checks and docs
        if request.url.path in ["/", "/docs", "/redoc", "/openapi.json"]:
            response = await call_next(request)
            return response
        
        # Apply rate limiting
        client_ip = request.client.host
        if not rate_limiter.is_allowed(client_ip):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded. Please try again later."
            )
        
        response = await call_next(request)
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Rate limiting middleware error: {e}")
        response = await call_next(request)
        return response

# Error handling middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Log successful requests
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            extra={
                "method": request.method,
                "url": str(request.url),
                "status_code": response.status_code,
                "process_time": round(process_time, 4),
                "timestamp": datetime.utcnow().isoformat(),
            }
        )
        
        return response
        
    except Exception as exc:
        process_time = time.time() - start_time
        logger.error(
            "Request failed",
            extra={
                "method": request.method,
                "url": str(request.url),
                "error": str(exc),
                "error_type": type(exc).__name__,
                "process_time": round(process_time, 4),
                "timestamp": datetime.utcnow().isoformat(),
            },
            exc_info=True
        )
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": "An unexpected error occurred",
                "timestamp": datetime.utcnow().isoformat(),
            }
        )

# Include routers
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api", tags=["authentication"])
app.include_router(projects_router, prefix="/api", tags=["projects"])
app.include_router(content_router, prefix="/api", tags=["content"])

# Root endpoint
@app.get("/")
async def root():
    """
    Welcome endpoint for CodeBridge API
    """
    return {
        "message": "🌉 Welcome to CodeBridge API",
        "description": "README-to-Blog Automation Platform",
        "version": settings.VERSION,
        "status": "running",
        "timestamp": datetime.utcnow().isoformat(),
        "endpoints": {
            "docs": "/docs",
            "health": "/api/health",
            "authentication": "/api/auth/login",
            "projects": "/api/projects",
            "content": "/api/content"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_config=None,  # We handle logging ourselves
    )
