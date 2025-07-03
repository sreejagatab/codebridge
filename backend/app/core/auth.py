"""
Authentication and Authorization Middleware
"""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List
import logging

from ..core.config import settings
from ..models.schemas import TokenData, User

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer token scheme
security = HTTPBearer()

# JWT Configuration
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthenticationError(HTTPException):
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class AuthorizationError(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        permissions: List[str] = payload.get("permissions", [])
        
        if username is None:
            raise AuthenticationError()
            
        token_data = TokenData(username=username, permissions=permissions)
        return token_data
    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise AuthenticationError()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """Get current authenticated user from JWT token"""
    return verify_token(credentials.credentials)


async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    """Get current active user (can be extended with database lookup)"""
    # In a real implementation, you would fetch user from database
    # and check if user is active
    return current_user


class PermissionChecker:
    """Check if user has required permissions"""
    
    def __init__(self, required_permissions: List[str]):
        self.required_permissions = required_permissions
    
    def __call__(self, current_user: TokenData = Depends(get_current_active_user)) -> TokenData:
        for permission in self.required_permissions:
            if permission not in current_user.permissions:
                raise AuthorizationError(
                    detail=f"Permission '{permission}' required"
                )
        return current_user


# Permission dependency factories
def require_permissions(*permissions: str):
    """Factory function to create permission dependency"""
    return Depends(PermissionChecker(list(permissions)))


# Common permission dependencies
require_admin = require_permissions("admin")
require_read = require_permissions("read")
require_write = require_permissions("write")
require_delete = require_permissions("delete")


# Optional authentication (for public endpoints with optional auth)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[TokenData]:
    """Get current user if authenticated, None otherwise"""
    if credentials is None:
        return None
    
    try:
        return verify_token(credentials.credentials)
    except AuthenticationError:
        return None


# Rate limiting setup (in-memory for now, should use Redis in production)
from collections import defaultdict
import time

class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        now = time.time()
        minute_ago = now - 60
        
        # Clean old requests
        self.requests[key] = [req_time for req_time in self.requests[key] if req_time > minute_ago]
        
        # Check if under limit
        if len(self.requests[key]) >= self.requests_per_minute:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


# Rate limiter instances
rate_limiter = RateLimiter(requests_per_minute=60)
strict_rate_limiter = RateLimiter(requests_per_minute=10)


async def check_rate_limit(request, call_next, limiter: RateLimiter = rate_limiter):
    """Rate limiting middleware"""
    client_ip = request.client.host
    
    if not limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )
    
    response = await call_next(request)
    return response


# Demo user for testing (in production, this would be in database)
DEMO_USERS = {
    "admin": {
        "username": "admin",
        "email": "admin@codebridge.com",
        "hashed_password": get_password_hash("admin123"),
        "permissions": ["admin", "read", "write", "delete"],
        "is_active": True
    },
    "user": {
        "username": "user",
        "email": "user@codebridge.com", 
        "hashed_password": get_password_hash("user123"),
        "permissions": ["read", "write"],
        "is_active": True
    }
}


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Authenticate user with username and password"""
    user = DEMO_USERS.get(username)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
        return None
    
    return user
