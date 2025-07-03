#!/usr/bin/env python3
"""
Verification script for CodeBridge Step 1 implementation
Tests all the requirements mentioned in you.md
"""

import sys
import os
import subprocess
import importlib.util
import json
from pathlib import Path

def test_project_structure():
    """Test if all required directories and files exist"""
    print("🔍 Testing project structure...")
    
    required_paths = [
        "backend/app/__init__.py",
        "backend/app/main.py", 
        "backend/app/core/config.py",
        "backend/app/core/logging_config.py",
        "backend/app/api/health.py",
        "backend/app/models/__init__.py",
        "backend/app/services/__init__.py",
        "backend/app/utils/__init__.py",
        "backend/tests/__init__.py",
        "backend/tests/test_health.py",
        "backend/requirements.txt",
        "backend/Dockerfile",
        "backend/docker-compose.yml",
        "backend/.env.example",
        "frontend/package.json",
        "frontend/Dockerfile",
        "frontend/src/index.js",
        "frontend/public/index.html",
        "docs/",
        "scripts/",
        "README.md"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print(f"❌ Missing files/directories: {missing_paths}")
        return False
    else:
        print("✅ All required files and directories exist")
        return True

def test_python_imports():
    """Test if Python modules can be imported"""
    print("🐍 Testing Python imports...")
    
    try:
        # Add backend to path
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        
        # Test imports
        from app.core.config import settings
        from app.core.logging_config import setup_logging
        
        print("✅ Core modules import successfully")
        print(f"   - App Name: {settings.APP_NAME}")
        print(f"   - Version: {settings.VERSION}")
        print(f"   - Debug: {settings.DEBUG}")
        print(f"   - Host: {settings.HOST}:{settings.PORT}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_fastapi_app():
    """Test if FastAPI app can be created"""
    print("🚀 Testing FastAPI application...")
    
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        from app.main import app
        
        print("✅ FastAPI app created successfully")
        print(f"   - Title: {app.title}")
        print(f"   - Version: {app.version}")
        
        # Check if routes exist
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/health", "/api/health/simple"]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Route {route} exists")
            else:
                print(f"   ❌ Route {route} missing")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def test_logging_configuration():
    """Test logging configuration"""
    print("📝 Testing logging configuration...")
    
    try:
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        from app.core.logging_config import setup_logging, JSONFormatter
        import logging
        
        # Setup logging
        logger = setup_logging()
        
        # Test JSON formatter
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="test.py",
            lineno=1,
            msg="Test message",
            args=(),
            exc_info=None
        )
        
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        required_fields = ["timestamp", "level", "logger", "message"]
        for field in required_fields:
            if field not in log_data:
                print(f"❌ Missing log field: {field}")
                return False
        
        print("✅ Logging configuration works")
        print(f"   - JSON format: {log_data['level']}")
        print(f"   - Timestamp: {log_data['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Logging error: {e}")
        return False

def test_docker_files():
    """Test Docker configuration"""
    print("🐳 Testing Docker configuration...")
    
    # Check Dockerfile
    with open("backend/Dockerfile", "r") as f:
        dockerfile_content = f.read()
        
    required_docker_elements = [
        "FROM python:3.11-slim",
        "WORKDIR /app",
        "COPY requirements.txt",
        "RUN pip install",
        "EXPOSE 8000",
        "HEALTHCHECK",
        "CMD"
    ]
    
    for element in required_docker_elements:
        if element in dockerfile_content:
            print(f"   ✅ {element} found in Dockerfile")
        else:
            print(f"   ❌ {element} missing from Dockerfile")
            return False
    
    # Check docker-compose.yml
    with open("backend/docker-compose.yml", "r") as f:
        compose_content = f.read()
        
    required_compose_elements = [
        "version:",
        "services:",
        "backend:",
        "build:",
        "ports:",
        "environment:",
        "healthcheck:"
    ]
    
    for element in required_compose_elements:
        if element in compose_content:
            print(f"   ✅ {element} found in docker-compose.yml")
        else:
            print(f"   ❌ {element} missing from docker-compose.yml")
            return False
    
    print("✅ Docker configuration is valid")
    return True

def main():
    """Run all tests"""
    print("🧪 CodeBridge Step 1 Verification")
    print("=" * 40)
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        test_project_structure,
        test_python_imports,
        test_fastapi_app,
        test_logging_configuration,
        test_docker_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    print("=" * 40)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Step 1 implementation is complete.")
        print("\nNext steps:")
        print("1. Copy .env.example to .env and configure")
        print("2. Install dependencies: pip install -r backend/requirements.txt")
        print("3. Run the application: uvicorn app.main:app --reload")
        print("4. Test endpoints: http://localhost:8000/api/health")
        print("5. Or use Docker: docker-compose up --build")
        return True
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    main()
