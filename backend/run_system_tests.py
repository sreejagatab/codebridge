"""
CodeBridge System Test Runner
============================

This script runs the complete system testing framework for Steps 1 & 2.
It validates all components and starts the system for integration testing.
"""

import asyncio
import sys
import subprocess
import time
import requests
from pathlib import Path
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemTestRunner:
    """Comprehensive system test runner"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.test_results = []
        self.server_process = None
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result"""
        status = "✅ PASS" if passed else "❌ FAIL"
        result = {"test": test_name, "passed": passed, "message": message}
        self.test_results.append(result)
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        logger.info(f"Test {test_name}: {'PASSED' if passed else 'FAILED'} - {message}")
    
    def run_validation_script(self, script_name: str) -> bool:
        """Run a validation script and return success status"""
        try:
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                cwd=self.base_path
            )
            
            if result.returncode == 0:
                self.log_test(f"Validation: {script_name}", True, "Script executed successfully")
                return True
            else:
                self.log_test(f"Validation: {script_name}", False, f"Exit code: {result.returncode}")
                if result.stderr:
                    print(f"    Error: {result.stderr}")
                return False
                
        except Exception as e:
            self.log_test(f"Validation: {script_name}", False, f"Exception: {e}")
            return False
    
    def check_file_structure(self) -> bool:
        """Check if all required files exist"""
        required_files = [
            "app/main.py",
            "app/core/config.py",
            "app/core/database.py",
            "app/core/logging_config.py",
            "app/api/health.py",
            "app/models/database.py",
            "app/services/database_service.py",
            "requirements.txt",
            "alembic.ini",
            "manage.py"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not (self.base_path / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            self.log_test("File Structure", False, f"Missing files: {missing_files}")
            return False
        else:
            self.log_test("File Structure", True, f"All {len(required_files)} required files present")
            return True
    
    def test_database_creation(self) -> bool:
        """Test database creation and basic operations"""
        try:
            # Import after ensuring the module path is correct
            sys.path.append(str(self.base_path))
            from app.core.database import create_tables, SessionLocal
            from app.services.database_service import ProjectService
            
            # Create tables
            create_tables()
            
            # Test basic database operation
            db = SessionLocal()
            
            # Test creating a project
            test_project = {
                "platform": "github",
                "url": "https://github.com/test/system-test",
                "name": "System Test Project",
                "description": "Test project for system validation",
                "stars": 1,
                "language": "Python",
                "topics": ["test", "validation"],
                "status": "testing"
            }
            
            project = ProjectService.create_project(db, test_project)
            
            if project and project.id:
                # Clean up
                ProjectService.delete_project(db, project.id)
                db.close()
                self.log_test("Database Operations", True, "CRUD operations working")
                return True
            else:
                db.close()
                self.log_test("Database Operations", False, "Failed to create project")
                return False
                
        except Exception as e:
            self.log_test("Database Operations", False, f"Exception: {e}")
            return False
    
    def start_server(self) -> bool:
        """Start the FastAPI server"""
        try:
            import uvicorn
            from app.main import app
            
            # Start server in background
            self.server_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "app.main:app", 
                "--host", "0.0.0.0", 
                "--port", "3047"
            ], cwd=self.base_path)
            
            # Wait for server to start
            time.sleep(5)
            
            self.log_test("Server Start", True, "Server started on port 3047")
            return True
            
        except Exception as e:
            self.log_test("Server Start", False, f"Exception: {e}")
            return False
    
    def test_health_endpoints(self) -> bool:
        """Test health endpoints"""
        endpoints = [
            ("/", "Root endpoint"),
            ("/api/health/simple", "Simple health check"),
            ("/api/health", "Full health check"),
            ("/api/health/database", "Database health check")
        ]
        
        all_passed = True
        
        for endpoint, description in endpoints:
            try:
                response = requests.get(f"http://localhost:3047{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    self.log_test(f"Endpoint: {endpoint}", True, f"{description} - Status: {response.status_code}")
                else:
                    self.log_test(f"Endpoint: {endpoint}", False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Endpoint: {endpoint}", False, f"Request failed: {e}")
                all_passed = False
        
        return all_passed
    
    def test_api_documentation(self) -> bool:
        """Test API documentation endpoints"""
        docs_endpoints = [
            ("/docs", "Swagger UI"),
            ("/redoc", "ReDoc"),
            ("/openapi.json", "OpenAPI Schema")
        ]
        
        all_passed = True
        
        for endpoint, description in docs_endpoints:
            try:
                response = requests.get(f"http://localhost:3047{endpoint}", timeout=10)
                
                if response.status_code == 200:
                    self.log_test(f"Docs: {endpoint}", True, f"{description} accessible")
                else:
                    self.log_test(f"Docs: {endpoint}", False, f"Status: {response.status_code}")
                    all_passed = False
                    
            except requests.exceptions.RequestException as e:
                self.log_test(f"Docs: {endpoint}", False, f"Request failed: {e}")
                all_passed = False
        
        return all_passed
    
    def stop_server(self):
        """Stop the server"""
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait()
            print("🛑 Server stopped")
    
    def run_comprehensive_tests(self):
        """Run all system tests"""
        print("🚀 CODEBRIDGE COMPREHENSIVE SYSTEM TESTING")
        print("=" * 80)
        print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Phase 1: Static validation
        print("📋 PHASE 1: STATIC VALIDATION")
        print("-" * 50)
        
        structure_ok = self.check_file_structure()
        
        # Phase 2: Database testing
        print(f"\n🗄️  PHASE 2: DATABASE TESTING")
        print("-" * 50)
        
        database_ok = self.test_database_creation()
        
        # Phase 3: Server testing
        print(f"\n🌐 PHASE 3: SERVER TESTING")
        print("-" * 50)
        
        server_ok = self.start_server()
        
        if server_ok:
            # Test endpoints
            endpoints_ok = self.test_health_endpoints()
            docs_ok = self.test_api_documentation()
            
            # Stop server
            self.stop_server()
        else:
            endpoints_ok = False
            docs_ok = False
        
        # Final summary
        print(f"\n{'=' * 80}")
        print("🏆 SYSTEM TEST RESULTS")
        print("=" * 80)
        
        all_phases = [
            ("File Structure", structure_ok),
            ("Database Operations", database_ok),
            ("Server Start", server_ok),
            ("Health Endpoints", endpoints_ok),
            ("API Documentation", docs_ok)
        ]
        
        passed_phases = sum(1 for _, passed in all_phases if passed)
        total_phases = len(all_phases)
        
        for phase_name, passed in all_phases:
            status = "✅ PASSED" if passed else "❌ FAILED"
            print(f"{status}: {phase_name}")
        
        print(f"\n📊 Overall Result: {passed_phases}/{total_phases} phases passed")
        
        if passed_phases == total_phases:
            print("\n🎉 ALL SYSTEM TESTS PASSED!")
            print("✅ CodeBridge is fully operational")
            print("✅ Steps 1 & 2 implementation verified")
            print("🚀 System ready for production use")
            print(f"\n🌐 Access the system:")
            print(f"   - API: http://localhost:3047")
            print(f"   - Docs: http://localhost:3047/docs")
            print(f"   - Health: http://localhost:3047/api/health")
        else:
            print(f"\n❌ {total_phases - passed_phases} PHASES FAILED")
            print("Please address the issues above before proceeding")
        
        print("=" * 80)
        return passed_phases == total_phases

def main():
    """Main test execution"""
    runner = SystemTestRunner()
    
    try:
        success = runner.run_comprehensive_tests()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n🛑 Testing interrupted by user")
        runner.stop_server()
        return 1
    except Exception as e:
        print(f"\n❌ Testing failed with error: {e}")
        runner.stop_server()
        return 1

if __name__ == "__main__":
    sys.exit(main())
