"""
Simple database test to verify Step 2 setup
"""

import sys
from pathlib import Path
import asyncio
import logging

# Add current directory to Python path
sys.path.append(str(Path(__file__).parent))

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all imports work"""
    try:
        from app.core.database import SessionLocal, create_tables
        from app.models.database import Project, Content, Base
        from app.services.database_service import ProjectService, ContentService
        logger.info("✅ All imports successful")
        return True
    except Exception as e:
        logger.error(f"❌ Import failed: {e}")
        return False

def test_database_creation():
    """Test database and table creation"""
    try:
        from app.core.database import create_tables
        create_tables()
        logger.info("✅ Database tables created successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database creation failed: {e}")
        return False

def test_basic_crud():
    """Test basic CRUD operations"""
    try:
        from app.core.database import SessionLocal
        from app.services.database_service import ProjectService, ContentService
        
        db = SessionLocal()
        
        # Test project creation
        project_data = {
            "platform": "github",
            "url": "https://github.com/test/simple-test",
            "name": "Simple Test Project",
            "description": "A test project for Step 2",
            "stars": 1,
            "language": "Python",
            "topics": ["test", "demo"],
            "status": "testing"
        }
        
        project = ProjectService.create_project(db, project_data)
        logger.info(f"✅ Project created: {project.name} (ID: {project.id})")
        
        # Test content creation
        content_data = {
            "project_id": project.id,
            "content_type": "test",
            "title": "Test Content",
            "slug": "test-content-simple",
            "raw_content": "This is test content",
            "tags": ["test"]
        }
        
        content = ContentService.create_content(db, content_data)
        logger.info(f"✅ Content created: {content.title} (ID: {content.id})")
        
        # Test reading
        retrieved_project = ProjectService.get_project(db, project.id)
        retrieved_content = ContentService.get_content(db, content.id)
        
        if retrieved_project and retrieved_content:
            logger.info("✅ CRUD operations successful")
            
            # Test topics/tags handling
            logger.info(f"✅ Project topics: {retrieved_project.topics_list}")
            logger.info(f"✅ Content tags: {retrieved_content.tags_list}")
            
            db.close()
            return True
        else:
            logger.error("❌ Could not retrieve created records")
            db.close()
            return False
            
    except Exception as e:
        logger.error(f"❌ CRUD test failed: {e}")
        return False

async def test_async_connection():
    """Test async database connection"""
    try:
        from app.core.database import test_connection
        result = await test_connection()
        if result:
            logger.info("✅ Async database connection successful")
        else:
            logger.error("❌ Async database connection failed")
        return result
    except Exception as e:
        logger.error(f"❌ Async connection test error: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting Simple Database Tests for Step 2")
    logger.info("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Creation", test_database_creation),
        ("CRUD Operations", test_basic_crud),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n🔧 Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                logger.error(f"❌ {test_name} failed")
        except Exception as e:
            logger.error(f"❌ {test_name} error: {e}")
    
    # Test async connection
    logger.info(f"\n🔧 Running: Async Connection Test")
    try:
        async_result = asyncio.run(test_async_connection())
        if async_result:
            passed += 1
        total += 1
    except Exception as e:
        logger.error(f"❌ Async Connection Test error: {e}")
        total += 1
    
    logger.info(f"\n" + "=" * 50)
    logger.info(f"📊 RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Step 2 database foundation is working!")
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
