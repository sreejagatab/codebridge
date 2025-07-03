"""
Test health endpoints
"""

import pytest
from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data
    assert "app_name" in data
    assert "system" in data
    assert "performance" in data


def test_simple_health_check(client: TestClient):
    """Test the simple health check endpoint"""
    response = client.get("/api/health/simple")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert data["message"] == "Service is running"


def test_root_endpoint(client: TestClient):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "status" in data
    assert "timestamp" in data
    assert data["message"] == "Welcome to CodeBridge API"
