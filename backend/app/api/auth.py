"""
Authentication API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import logging

from ..core.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from ..models.schemas import Token, APIResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user and return JWT access token.
    
    Use username and password to get an access token for API access.
    
    **Demo Credentials:**
    - Username: `admin`, Password: `admin123` (admin permissions)
    - Username: `user`, Password: `user123` (read/write permissions)
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user["username"],
            "permissions": user["permissions"]
        },
        expires_delta=access_token_expires
    )
    
    logger.info(
        f"User logged in: {user['username']}",
        extra={
            "username": user["username"],
            "permissions": user["permissions"]
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert to seconds
    }


@router.get("/me", response_model=APIResponse)
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    """
    Get current user information from JWT token.
    
    This endpoint shows information about the currently authenticated user.
    """
    return APIResponse(
        success=True,
        message="User information retrieved successfully",
        data={
            "username": current_user.username,
            "permissions": current_user.permissions,
            "authenticated": True
        }
    )


@router.post("/logout", response_model=APIResponse)
async def logout():
    """
    Logout endpoint (token invalidation would be handled client-side).
    
    In a production system, you might maintain a token blacklist.
    For now, this is a placeholder that instructs the client to discard the token.
    """
    return APIResponse(
        success=True,
        message="Logout successful. Please discard your access token.",
        data={"logged_out": True}
    )


# Import at the end to avoid circular imports
from ..core.auth import get_current_active_user
