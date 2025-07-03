"""
Test configuration for pytest
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app


@pytest.fixture
def client():
    """Create a test client"""
    return TestClient(app)


@pytest.fixture
def test_settings():
    """Test settings override"""
    from app.core.config import settings
    settings.DEBUG = True
    settings.LOG_LEVEL = "DEBUG"
    return settings
