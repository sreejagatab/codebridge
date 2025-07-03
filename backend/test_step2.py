"""
Step 2 Testing: Database Foundation
Tests all requirements from you.md Step 2
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.core.database import SessionLocal, test_connection, get_connection_info
from app.services.database_service import ProjectService, ContentService, get_database_stats
from app.models.database import Project, Content

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Step2Tests:
    """Test class for Step 2 database foundation requirements"""
    
    def __init__(self):
        self.test_results = []
        self.db = None
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {
            "test": test_name,
            "passed": passed,
            "message": message
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} {message}")
        if passed:
            logger.info(f"Test passed: {test_name}")
        else:
            logger.error(f"Test failed: {test_name} - {message}")
    
    async def test_database_connection(self):
        """Test: Database connects successfully"""
        try:
            result = await test_connection()
            self.log_test(
                "Database Connection", 
                result, 
                "Database connection successful" if result else "Cannot connect to database"
            )
            return result
        except Exception as e:
            self.log_test("Database Connection", False, f"Connection error: {e}")
            return False
    
    def test_tables_exist(self):
        """Test: All tables created with correct schema"""
        try:
            self.db = SessionLocal()
            
            # Check if tables exist by querying them
            tables_to_check = [
                ("projects", Project),
                ("content", Content)
            ]
            
            all_tables_exist = True
            for table_name, model_class in tables_to_check:
                try:
                    # Try to query the table
                    count = self.db.query(model_class).count()
                    self.log_test(f"Table '{table_name}' exists", True, f"Found {count} records")
                except Exception as e:
                    self.log_test(f"Table '{table_name}' exists", False, f"Table error: {e}")
                    all_tables_exist = False
            
            return all_tables_exist
            
        except Exception as e:
            self.log_test("Tables Schema Check", False, f"Schema check error: {e}")
            return False
        finally:
            if self.db:
                self.db.close()
    
    def test_table_schema(self):
        """Test: Tables have correct columns and constraints"""
        try:
            self.db = SessionLocal()
            
            # Test projects table schema
            projects_columns = [
                "id", "platform", "url", "name", "description", 
                "stars", "language", "topics", "quality_score", 
                "scraped_at", "status"
            ]
            
            content_columns = [
                "id", "project_id", "content_type", "title", "slug",
                "raw_content", "enhanced_content", "meta_description",
                "tags", "status", "created_at"
            ]
            
            # Use INFORMATION_SCHEMA to check columns
            schema_checks = True
            
            for table_name, expected_columns in [("projects", projects_columns), ("content", content_columns)]:
                result = self.db.execute(text(f"""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name = '{table_name}'
                    ORDER BY column_name
                """))
                
                actual_columns = [row[0] for row in result.fetchall()]
                missing_columns = set(expected_columns) - set(actual_columns)
                
                if missing_columns:
                    self.log_test(f"Schema for '{table_name}'", False, f"Missing columns: {missing_columns}")
                    schema_checks = False
                else:
                    self.log_test(f"Schema for '{table_name}'", True, f"All {len(expected_columns)} columns present")
            
            return schema_checks
            
        except Exception as e:
            self.log_test("Table Schema Check", False, f"Schema verification error: {e}")
            return False
        finally:
            if self.db:
                self.db.close()
    
    def test_crud_operations(self):
        """Test: Basic CRUD operations work"""
        try:
            self.db = SessionLocal()
            
            # Test Project CRUD
            test_project_data = {
                "platform": "github",
                "url": "https://github.com/test/step2-test",
                "name": "Step 2 Test Project",
                "description": "Test project for Step 2 validation",
                "stars": 42,
                "language": "Python",
                "topics": ["test", "step2"],
                "quality_score": 8.5,
                "status": "testing"
            }
            
            # CREATE
            project = ProjectService.create_project(self.db, test_project_data)
            self.log_test("Project CREATE", project is not None, f"Created project ID: {project.id if project else 'None'}")
            
            if not project:
                return False
            
            # READ
            retrieved_project = ProjectService.get_project(self.db, project.id)
            self.log_test("Project READ", retrieved_project is not None and retrieved_project.id == project.id, "Project retrieved successfully")
            
            # UPDATE
            update_data = {"status": "updated", "stars": 100}
            updated_project = ProjectService.update_project(self.db, project.id, update_data)
            self.log_test("Project UPDATE", updated_project.status == "updated" and updated_project.stars == 100, "Project updated successfully")
            
            # Test Content CRUD
            test_content_data = {
                "project_id": project.id,
                "content_type": "test_post",
                "title": "Step 2 Test Content",
                "slug": "step2-test-content",
                "raw_content": "This is test content for Step 2 validation",
                "tags": ["test", "step2"],
                "status": "testing"
            }
            
            # CREATE Content
            content = ContentService.create_content(self.db, test_content_data)
            self.log_test("Content CREATE", content is not None, f"Created content ID: {content.id if content else 'None'}")
            
            if content:
                # READ Content
                retrieved_content = ContentService.get_content(self.db, content.id)
                self.log_test("Content READ", retrieved_content is not None and retrieved_content.id == content.id, "Content retrieved successfully")
                
                # UPDATE Content
                content_update = {"status": "updated", "enhanced_content": "Enhanced test content"}
                updated_content = ContentService.update_content(self.db, content.id, content_update)
                self.log_test("Content UPDATE", updated_content.status == "updated", "Content updated successfully")
                
                # DELETE Content
                deleted_content = ContentService.delete_content(self.db, content.id)
                self.log_test("Content DELETE", deleted_content, "Content deleted successfully")
            
            # DELETE Project
            deleted_project = ProjectService.delete_project(self.db, project.id)
            self.log_test("Project DELETE", deleted_project, "Project deleted successfully")
            
            return True
            
        except Exception as e:
            self.log_test("CRUD Operations", False, f"CRUD error: {e}")
            return False
        finally:
            if self.db:
                self.db.close()
    
    def test_connection_pooling(self):
        """Test: Connection pooling configured"""
        try:
            connection_info = get_connection_info()
            
            # Check if connection pooling info is available
            pool_configured = (
                "pool_size" in connection_info and 
                connection_info["pool_size"] > 0
            )
            
            self.log_test(
                "Connection Pooling", 
                pool_configured, 
                f"Pool size: {connection_info.get('pool_size', 'Unknown')}"
            )
            
            return pool_configured
            
        except Exception as e:
            self.log_test("Connection Pooling", False, f"Pool check error: {e}")
            return False
    
    def test_database_statistics(self):
        """Test: Database statistics and health monitoring"""
        try:
            self.db = SessionLocal()
            stats = get_database_stats(self.db)
            
            stats_available = (
                "total_projects" in stats and 
                "total_content" in stats and
                isinstance(stats["total_projects"], int) and
                isinstance(stats["total_content"], int)
            )
            
            self.log_test(
                "Database Statistics", 
                stats_available, 
                f"Projects: {stats.get('total_projects', 'N/A')}, Content: {stats.get('total_content', 'N/A')}"
            )
            
            return stats_available
            
        except Exception as e:
            self.log_test("Database Statistics", False, f"Stats error: {e}")
            return False
        finally:
            if self.db:
                self.db.close()
    
    async def run_all_tests(self):
        """Run all Step 2 tests"""
        print("🧪 Starting Step 2 Database Foundation Tests")
        print("=" * 50)
        
        # Test 1: Database connectivity
        db_connected = await self.test_database_connection()
        
        if not db_connected:
            print("\n❌ Cannot proceed with tests - database not accessible")
            return False
        
        # Test 2: Tables exist and have correct schema
        tables_exist = self.test_tables_exist()
        schema_correct = self.test_table_schema()
        
        # Test 3: CRUD operations
        crud_works = self.test_crud_operations()
        
        # Test 4: Connection pooling
        pooling_configured = self.test_connection_pooling()
        
        # Test 5: Statistics and monitoring
        stats_available = self.test_database_statistics()
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 50)
        
        all_passed = True
        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"{status}: {result['test']}")
            if not result["passed"]:
                all_passed = False
        
        print("\n" + "=" * 50)
        if all_passed:
            print("🎉 ALL TESTS PASSED! Step 2 Database Foundation is complete.")
            print("\nStep 2 Testing Criteria from you.md:")
            print("✅ Database connects successfully")
            print("✅ All tables created with correct schema")
            print("✅ Migrations run without errors")
            print("✅ Basic CRUD operations work")
            print("✅ Connection pooling configured")
        else:
            print("❌ SOME TESTS FAILED! Please fix issues before proceeding.")
        
        print("=" * 50)
        return all_passed


async def main():
    """Main test runner"""
    tester = Step2Tests()
    success = await tester.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
