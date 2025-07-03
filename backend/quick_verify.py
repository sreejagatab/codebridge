"""
Quick System Verification
=========================

This script performs a quick verification that all components are working.
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

def quick_test():
    """Perform quick system verification"""
    print("🔍 QUICK SYSTEM VERIFICATION")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Import core modules
    print("\n1. Testing core imports...")
    try:
        from app.main import app
        from app.core.config import settings
        print(f"   ✅ FastAPI app: {settings.APP_NAME} v{settings.VERSION}")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
    
    # Test 2: Database imports
    print("\n2. Testing database imports...")
    try:
        from app.core.database import SessionLocal, create_tables
        from app.models.database import Project, Content
        print("   ✅ Database modules imported")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Database import failed: {e}")
    
    # Test 3: Service imports
    print("\n3. Testing service imports...")
    try:
        from app.services.database_service import ProjectService, ContentService
        print("   ✅ Service modules imported")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Service import failed: {e}")
    
    # Test 4: Configuration
    print("\n4. Testing configuration...")
    try:
        from app.core.config import settings
        print(f"   ✅ Host: {settings.HOST}:{settings.PORT}")
        print(f"   ✅ Database: {settings.DATABASE_URL}")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Configuration failed: {e}")
    
    # Test 5: Database creation
    print("\n5. Testing database creation...")
    try:
        from app.core.database import create_tables
        create_tables()
        print("   ✅ Database tables created")
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Database creation failed: {e}")
    
    # Test 6: Basic CRUD
    print("\n6. Testing basic database operations...")
    try:
        from app.core.database import SessionLocal
        from app.services.database_service import ProjectService
        
        db = SessionLocal()
        
        # Count existing projects
        projects = ProjectService.get_projects(db, limit=10)
        print(f"   ✅ Found {len(projects)} projects in database")
        
        db.close()
        tests_passed += 1
    except Exception as e:
        print(f"   ❌ Database operations failed: {e}")
    
    # Summary
    print(f"\n{'=' * 40}")
    print(f"📊 VERIFICATION RESULTS: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("✅ System is ready to run")
        print("\n🚀 To start the server:")
        print("   run_full_system.bat")
        print("\n🧪 To test endpoints:")
        print("   python test_endpoints.py")
    else:
        print(f"❌ {total_tests - tests_passed} tests failed")
        print("Please check the errors above")
    
    print("=" * 40)
    return tests_passed == total_tests

if __name__ == "__main__":
    success = quick_test()
    input("\nPress Enter to continue...")
    sys.exit(0 if success else 1)
