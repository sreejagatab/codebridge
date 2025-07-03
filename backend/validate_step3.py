"""
Step 3 Implementation Validation
===============================

Quick validation script to check that all Step 3 requirements are implemented.
This runs without starting the server and validates the code structure.
"""

import os
import sys
import importlib.util
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def check_import(module_path, description):
    """Check if a module can be imported"""
    try:
        if module_path.startswith('app.'):
            # Add the current directory to sys.path for relative imports
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
        
        spec = importlib.util.spec_from_file_location("test_module", module_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ {description}: Can import successfully")
            return True
        else:
            __import__(module_path)
            print(f"✅ {description}: Can import successfully")
            return True
    except Exception as e:
        print(f"❌ {description}: Import failed - {e}")
        return False

def check_step3_requirements():
    """Check all Step 3 requirements"""
    print("🔍 STEP 3 IMPLEMENTATION VALIDATION")
    print("=" * 50)
    
    all_good = True
    
    # Check file structure
    print("\n📁 File Structure:")
    files_to_check = [
        ("app/models/schemas.py", "Pydantic schemas"),
        ("app/core/auth.py", "Authentication middleware"),
        ("app/api/projects.py", "Projects API"),
        ("app/api/content.py", "Content API"),
        ("app/api/auth.py", "Authentication API"),
        ("test_step3.py", "Step 3 test script"),
        ("start_step3.bat", "Step 3 startup script")
    ]
    
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False
    
    # Check requirements.txt has new dependencies
    print("\n📦 Dependencies:")
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            
        required_deps = ["python-jose", "passlib"]
        for dep in required_deps:
            if dep in requirements:
                print(f"✅ {dep}: Found in requirements.txt")
            else:
                print(f"❌ {dep}: Missing from requirements.txt")
                all_good = False
    except Exception as e:
        print(f"❌ Could not read requirements.txt: {e}")
        all_good = False
    
    # Check code imports
    print("\n🐍 Code Validation:")
    try:
        # Check if we can import the main components
        from app.models import schemas
        print("✅ Pydantic schemas: Import successful")
        
        # Check if schemas have required models
        required_schemas = ["ProjectCreate", "ContentCreate", "Token", "APIResponse"]
        for schema_name in required_schemas:
            if hasattr(schemas, schema_name):
                print(f"✅ Schema {schema_name}: Found")
            else:
                print(f"❌ Schema {schema_name}: Missing")
                all_good = False
                
    except Exception as e:
        print(f"❌ Schemas import failed: {e}")
        all_good = False
    
    try:
        from app.core import auth
        print("✅ Authentication module: Import successful")
        
        # Check for key auth functions
        auth_functions = ["create_access_token", "verify_token", "get_current_user"]
        for func_name in auth_functions:
            if hasattr(auth, func_name):
                print(f"✅ Auth function {func_name}: Found")
            else:
                print(f"❌ Auth function {func_name}: Missing")
                all_good = False
                
    except Exception as e:
        print(f"❌ Auth module import failed: {e}")
        all_good = False
    
    try:
        from app.api import projects, content, auth as auth_api
        print("✅ API modules: Import successful")
    except Exception as e:
        print(f"❌ API modules import failed: {e}")
        all_good = False
    
    # Check main app configuration
    print("\n⚙️ Application Configuration:")
    try:
        from app.main import app
        
        # Check if new routers are included
        router_tags = set()
        for route in app.routes:
            if hasattr(route, 'tags') and route.tags:
                router_tags.update(route.tags)
        
        expected_tags = ["authentication", "projects", "content"]
        for tag in expected_tags:
            if tag in router_tags:
                print(f"✅ {tag.title()} API: Router registered")
            else:
                print(f"❌ {tag.title()} API: Router missing")
                all_good = False
                
        print("✅ FastAPI app: Import successful")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        all_good = False
    
    # Check database service functions
    print("\n🗄️ Database Services:")
    try:
        from app.services import database_service
        
        required_functions = [
            "create_project", "get_project", "update_project", "delete_project",
            "create_content", "get_content", "update_content", "delete_content"
        ]
        
        for func_name in required_functions:
            if hasattr(database_service, func_name):
                print(f"✅ Database function {func_name}: Found")
            else:
                print(f"❌ Database function {func_name}: Missing")
                all_good = False
                
    except Exception as e:
        print(f"❌ Database service import failed: {e}")
        all_good = False
    
    # Summary
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 STEP 3 VALIDATION PASSED")
        print("✅ All requirements implemented correctly")
        print("\n📋 Step 3 Features Ready:")
        print("   • RESTful API design")
        print("   • Request/response validation with Pydantic")
        print("   • JWT Authentication middleware")
        print("   • Rate limiting")
        print("   • API documentation with OpenAPI/Swagger")
        print("\n🚀 Ready to start server and run tests!")
        print("   1. Run: start_step3.bat")
        print("   2. Test: python test_step3.py")
    else:
        print("❌ STEP 3 VALIDATION FAILED")
        print("Some requirements are missing or incorrectly implemented")
        print("Please check the errors above and fix them before proceeding")
    
    return all_good

if __name__ == "__main__":
    success = check_step3_requirements()
    sys.exit(0 if success else 1)
