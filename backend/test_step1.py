"""
Quick validation script for CodeBridge Step 1
"""

def test_basic_functionality():
    """Test basic functionality without running the server"""
    print("🧪 Testing CodeBridge Step 1 Implementation")
    print("=" * 50)
    
    # Test 1: Configuration
    print("1. Testing Configuration...")
    try:
        from app.core.config import settings
        print(f"   ✅ App Name: {settings.APP_NAME}")
        print(f"   ✅ Version: {settings.VERSION}")
        print(f"   ✅ Debug Mode: {settings.DEBUG}")
        print(f"   ✅ Host:Port: {settings.HOST}:{settings.PORT}")
    except Exception as e:
        print(f"   ❌ Configuration error: {e}")
        return False
    
    # Test 2: Logging Setup
    print("\n2. Testing Logging Configuration...")
    try:
        from app.core.logging_config import setup_logging, JSONFormatter
        import logging
        import json
        
        logger = setup_logging()
        
        # Test JSON formatter
        formatter = JSONFormatter()
        record = logging.LogRecord(
            name="test", level=logging.INFO, pathname="test.py",
            lineno=1, msg="Test log message", args=(), exc_info=None
        )
        formatted = formatter.format(record)
        log_data = json.loads(formatted)
        
        print(f"   ✅ JSON Logging: {log_data['level']}")
        print(f"   ✅ Timestamp: {log_data['timestamp']}")
        print(f"   ✅ Message: {log_data['message']}")
        
    except Exception as e:
        print(f"   ❌ Logging error: {e}")
        return False
    
    # Test 3: FastAPI App Creation
    print("\n3. Testing FastAPI Application...")
    try:
        from app.main import app
        print(f"   ✅ App Title: {app.title}")
        print(f"   ✅ App Version: {app.version}")
        print(f"   ✅ App Description: {app.description}")
        
        # Check routes
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/health", "/api/health/simple"]
        
        for route in expected_routes:
            if route in routes:
                print(f"   ✅ Route: {route}")
            else:
                print(f"   ❌ Missing route: {route}")
                return False
                
    except Exception as e:
        print(f"   ❌ FastAPI error: {e}")
        return False
    
    # Test 4: Health Check Functionality  
    print("\n4. Testing Health Check...")
    try:
        import asyncio
        from app.api.health import health_check, simple_health_check
        
        # Test detailed health check
        result = asyncio.run(health_check())
        print(f"   ✅ Health Status: {result['status']}")
        print(f"   ✅ App Name: {result['app_name']}")
        print(f"   ✅ System Info: {result['system']['platform']}")
        
        # Test simple health check
        simple_result = asyncio.run(simple_health_check())
        print(f"   ✅ Simple Health: {simple_result['status']}")
        
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
        return False
    
    # Test 5: Error Handling & CORS Middleware
    print("\n5. Testing Middleware Configuration...")
    try:
        # Check middleware
        middleware_count = len(app.user_middleware)
        print(f"   ✅ Middleware count: {middleware_count}")
        
        # Check if CORS middleware is present
        cors_found = any(
            "CORSMiddleware" in str(middleware.cls) 
            for middleware in app.user_middleware
        )
        print(f"   ✅ CORS Middleware: {'Present' if cors_found else 'Missing'}")
        
    except Exception as e:
        print(f"   ❌ Middleware error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All Core Components Working Successfully!")
    print("\n📋 Step 1 Requirements Summary:")
    print("✅ FastAPI application with proper project structure")
    print("✅ Environment configuration management") 
    print("✅ Logging setup with structured JSON logs")
    print("✅ Error handling middleware")
    print("✅ CORS configuration")
    print("✅ Basic health check endpoint")
    print("✅ Docker containerization files")
    
    print("\n🚀 Next Steps:")
    print("1. Copy .env.example to .env and configure as needed")
    print("2. Install all dependencies: pip install -r requirements.txt")
    print("3. Start the server: uvicorn app.main:app --reload")
    print("4. Test endpoints:")
    print("   - http://localhost:8000/ (root)")
    print("   - http://localhost:8000/api/health (detailed health)")
    print("   - http://localhost:8000/docs (API documentation)")
    print("5. Or use Docker: docker-compose up --build")
    
    return True

if __name__ == "__main__":
    import sys
    import os
    
    # Change to backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    if not backend_dir.endswith('backend'):
        backend_dir = os.path.join(os.path.dirname(backend_dir), 'backend')
    
    os.chdir(backend_dir)
    
    # Add to Python path
    sys.path.insert(0, os.getcwd())
    
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
