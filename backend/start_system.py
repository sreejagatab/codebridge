"""
Simple System Startup and Test
==============================

This script provides a simple way to start and test the CodeBridge system.
It includes basic validation and server startup.
"""

import sys
import time
from pathlib import Path

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test that all core modules can be imported"""
    print("🔧 Testing imports...")
    
    try:
        from app.main import app
        from app.core.config import settings
        from app.core.database import SessionLocal, create_tables
        from app.models.database import Project, Content
        from app.services.database_service import ProjectService, ContentService
        print("✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def setup_database():
    """Setup database and test basic operations"""
    print("🗄️  Setting up database...")
    
    try:
        from app.core.database import create_tables, SessionLocal
        from app.services.database_service import ProjectService, seed_database
        
        # Create tables
        create_tables()
        print("✅ Database tables created")
        
        # Test database connection
        db = SessionLocal()
        
        # Run seeding
        seed_database(db)
        print("✅ Database seeded with sample data")
        
        # Test a basic query
        projects = ProjectService.get_projects(db, limit=5)
        print(f"✅ Database query successful - found {len(projects)} projects")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def validate_configuration():
    """Validate configuration settings"""
    print("⚙️ Validating configuration...")
    
    try:
        from app.core.config import settings
        
        print(f"   App Name: {settings.APP_NAME}")
        print(f"   Version: {settings.VERSION}")
        print(f"   Host: {settings.HOST}")
        print(f"   Port: {settings.PORT}")
        print(f"   Debug: {settings.DEBUG}")
        print(f"   Database URL: {settings.DATABASE_URL}")
        
        print("✅ Configuration validated")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    
    try:
        import uvicorn
        from app.main import app
        from app.core.config import settings
        
        print(f"\n🌐 Server starting on http://{settings.HOST}:{settings.PORT}")
        print("📚 API Documentation: http://localhost:3047/docs")
        print("🏥 Health Check: http://localhost:3047/api/health")
        print("🗄️  Database Health: http://localhost:3047/api/health/database")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        uvicorn.run(
            app,
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False
    
    return True

def main():
    """Main execution function"""
    print("🚀 CODEBRIDGE SYSTEM STARTUP")
    print("=" * 50)
    print(f"🕐 Starting at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run validation steps
    steps = [
        ("Import Testing", test_imports),
        ("Configuration Validation", validate_configuration),
        ("Database Setup", setup_database),
    ]
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        print("-" * 30)
        
        if not step_func():
            print(f"\n❌ {step_name} failed. Cannot proceed.")
            return False
    
    print(f"\n✅ All validation steps passed!")
    print("🎉 System is ready to start!")
    print()
    
    # Start the server
    start_server()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
