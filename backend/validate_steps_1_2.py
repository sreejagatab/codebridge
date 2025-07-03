"""
Steps 1 & 2 Comprehensive Validation
===================================

This script validates that both Step 1 (Project Skeleton Setup) and 
Step 2 (Database Foundation) are fully implemented according to you.md
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime

def validate_project_structure():
    """Validate Step 1: Project Skeleton Setup"""
    print("🏗️  STEP 1: PROJECT SKELETON SETUP VALIDATION")
    print("=" * 60)
    
    required_structure = {
        "backend/app/__init__.py": "Backend app package",
        "backend/app/main.py": "FastAPI main application",
        "backend/app/core/": "Core configuration directory",
        "backend/app/api/": "API routes directory", 
        "backend/app/models/": "Database models directory",
        "backend/app/services/": "Business logic services directory",
        "backend/app/utils/": "Utility functions directory",
        "backend/tests/": "Test files directory",
        "backend/requirements.txt": "Python dependencies",
        "backend/Dockerfile": "Backend Docker configuration",
        "backend/docker-compose.yml": "Docker compose configuration",
        "frontend/src/": "Frontend source directory",
        "frontend/public/": "Frontend public assets",
        "frontend/package.json": "Frontend dependencies",
        "frontend/Dockerfile": "Frontend Docker configuration",
        "docs/": "Documentation directory",
        "scripts/": "Project scripts directory",
        "README.md": "Project documentation"
    }
    
    missing = []
    present = []
    
    base_path = Path(__file__).parent.parent
    
    for path, description in required_structure.items():
        full_path = base_path / path
        if full_path.exists():
            present.append((path, description))
            print(f"✅ {path:<35} - {description}")
        else:
            missing.append((path, description))
            print(f"❌ {path:<35} - {description} (MISSING)")
    
    print(f"\n📊 Structure Validation: {len(present)}/{len(required_structure)} components present")
    
    if missing:
        print(f"⚠️  Missing components: {len(missing)}")
        return False
    else:
        print("🎉 All project structure components present!")
        return True

def validate_step1_implementation():
    """Validate Step 1 Implementation Requirements"""
    print(f"\n🔧 STEP 1: IMPLEMENTATION REQUIREMENTS")
    print("=" * 60)
    
    checks = []
    base_path = Path(__file__).parent
    
    # 1. FastAPI application with proper project structure
    main_py = base_path / "app" / "main.py"
    if main_py.exists():
        with open(main_py, 'r') as f:
            content = f.read()
            if "FastAPI" in content and "app = FastAPI" in content:
                checks.append(("FastAPI Application", True, "FastAPI app properly configured"))
            else:
                checks.append(("FastAPI Application", False, "FastAPI app not properly configured"))
    else:
        checks.append(("FastAPI Application", False, "main.py not found"))
    
    # 2. Environment configuration management
    config_py = base_path / "app" / "core" / "config.py"
    if config_py.exists():
        with open(config_py, 'r') as f:
            content = f.read()
            if "Settings" in content and "BaseSettings" in content:
                checks.append(("Environment Config", True, "Pydantic settings configured"))
            else:
                checks.append(("Environment Config", False, "Settings not properly configured"))
    else:
        checks.append(("Environment Config", False, "config.py not found"))
    
    # 3. Logging setup with structured JSON logs
    logging_py = base_path / "app" / "core" / "logging_config.py"
    if logging_py.exists():
        with open(logging_py, 'r') as f:
            content = f.read()
            if "json" in content.lower() and "logging" in content.lower():
                checks.append(("Structured Logging", True, "JSON logging configured"))
            else:
                checks.append(("Structured Logging", False, "JSON logging not configured"))
    else:
        checks.append(("Structured Logging", False, "logging_config.py not found"))
    
    # 4. Error handling middleware
    if main_py.exists():
        with open(main_py, 'r') as f:
            content = f.read()
            if "middleware" in content.lower() and "error" in content.lower():
                checks.append(("Error Handling", True, "Error middleware implemented"))
            else:
                checks.append(("Error Handling", False, "Error middleware not found"))
    
    # 5. CORS configuration
    if main_py.exists():
        with open(main_py, 'r') as f:
            content = f.read()
            if "CORSMiddleware" in content:
                checks.append(("CORS Configuration", True, "CORS middleware configured"))
            else:
                checks.append(("CORS Configuration", False, "CORS not configured"))
    
    # 6. Docker containerization
    dockerfile = base_path / "Dockerfile"
    if dockerfile.exists():
        checks.append(("Docker Container", True, "Dockerfile present"))
    else:
        checks.append(("Docker Container", False, "Dockerfile missing"))
    
    # 7. Basic health check endpoint
    health_py = base_path / "app" / "api" / "health.py"
    if health_py.exists():
        with open(health_py, 'r') as f:
            content = f.read()
            if "health" in content.lower() and "router" in content:
                checks.append(("Health Endpoint", True, "Health check endpoint implemented"))
            else:
                checks.append(("Health Endpoint", False, "Health endpoint not properly implemented"))
    else:
        checks.append(("Health Endpoint", False, "health.py not found"))
    
    # Print results
    passed = 0
    for check_name, status, message in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name:<20} - {message}")
        if status:
            passed += 1
    
    print(f"\n📊 Implementation Validation: {passed}/{len(checks)} requirements met")
    return passed == len(checks)

def validate_step2_database():
    """Validate Step 2: Database Foundation"""
    print(f"\n🗄️  STEP 2: DATABASE FOUNDATION VALIDATION") 
    print("=" * 60)
    
    checks = []
    base_path = Path(__file__).parent
    
    # 1. Database models exist
    models_py = base_path / "app" / "models" / "database.py"
    if models_py.exists():
        with open(models_py, 'r') as f:
            content = f.read()
            if "class Project" in content and "class Content" in content:
                checks.append(("Database Models", True, "Project and Content models defined"))
            else:
                checks.append(("Database Models", False, "Models not properly defined"))
    else:
        checks.append(("Database Models", False, "database.py not found"))
    
    # 2. Database connection and pooling
    database_py = base_path / "app" / "core" / "database.py"
    if database_py.exists():
        with open(database_py, 'r') as f:
            content = f.read()
            if "create_engine" in content and "pool" in content:
                checks.append(("Database Connection", True, "Connection pooling configured"))
            else:
                checks.append(("Database Connection", False, "Connection pooling not configured"))
    else:
        checks.append(("Database Connection", False, "database.py not found"))
    
    # 3. Alembic migrations
    alembic_ini = base_path / "alembic.ini"
    migration_dir = base_path / "alembic" / "versions"
    if alembic_ini.exists() and migration_dir.exists():
        migrations = list(migration_dir.glob("*.py"))
        if migrations:
            checks.append(("Migration System", True, f"{len(migrations)} migration(s) found"))
        else:
            checks.append(("Migration System", False, "No migrations found"))
    else:
        checks.append(("Migration System", False, "Alembic not properly configured"))
    
    # 4. CRUD operations
    service_py = base_path / "app" / "services" / "database_service.py" 
    if service_py.exists():
        with open(service_py, 'r') as f:
            content = f.read()
            if all(op in content for op in ["create_", "get_", "update_", "delete_"]):
                checks.append(("CRUD Operations", True, "Full CRUD operations implemented"))
            else:
                checks.append(("CRUD Operations", False, "CRUD operations incomplete"))
    else:
        checks.append(("CRUD Operations", False, "database_service.py not found"))
    
    # 5. Database seeding
    if service_py.exists():
        with open(service_py, 'r') as f:
            content = f.read()
            if "seed_database" in content:
                checks.append(("Database Seeding", True, "Seeding functionality implemented"))
            else:
                checks.append(("Database Seeding", False, "Seeding not implemented"))
    
    # 6. Check if database file exists (SQLite)
    db_file = base_path / "codebridge.db"
    if db_file.exists():
        checks.append(("Database File", True, "SQLite database file exists"))
        
        # Verify tables exist
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            if "projects" in tables and "content" in tables:
                checks.append(("Database Tables", True, f"Tables: {', '.join(tables)}"))
            else:
                checks.append(("Database Tables", False, f"Expected tables missing. Found: {tables}"))
            
            conn.close()
        except Exception as e:
            checks.append(("Database Tables", False, f"Error checking tables: {e}"))
    else:
        checks.append(("Database File", False, "Database file not created"))
    
    # Print results
    passed = 0
    for check_name, status, message in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name:<20} - {message}")
        if status:
            passed += 1
    
    print(f"\n📊 Database Validation: {passed}/{len(checks)} requirements met")
    return passed == len(checks)

def validate_integration():
    """Validate Integration between Step 1 and Step 2"""
    print(f"\n🔗 INTEGRATION VALIDATION")
    print("=" * 60)
    
    checks = []
    base_path = Path(__file__).parent
    
    # 1. Health endpoint includes database checks
    health_py = base_path / "app" / "api" / "health.py"
    if health_py.exists():
        with open(health_py, 'r') as f:
            content = f.read()
            if "database" in content.lower() and "get_db" in content:
                checks.append(("Health-DB Integration", True, "Health endpoint includes DB checks"))
            else:
                checks.append(("Health-DB Integration", False, "Health endpoint lacks DB integration"))
    
    # 2. Main app includes all routers
    main_py = base_path / "app" / "main.py"
    if main_py.exists():
        with open(main_py, 'r') as f:
            content = f.read()
            if "health_router" in content and "include_router" in content:
                checks.append(("Router Integration", True, "Health router properly included"))
            else:
                checks.append(("Router Integration", False, "Routers not properly included"))
    
    # 3. Configuration includes database settings
    config_py = base_path / "app" / "core" / "config.py"
    if config_py.exists():
        with open(config_py, 'r') as f:
            content = f.read()
            if "DATABASE_URL" in content:
                checks.append(("Config Integration", True, "Database configuration integrated"))
            else:
                checks.append(("Config Integration", False, "Database config missing"))
    
    # 4. Dependencies are complete
    requirements_txt = base_path / "requirements.txt" 
    if requirements_txt.exists():
        with open(requirements_txt, 'r') as f:
            content = f.read()
            required_deps = ["fastapi", "sqlalchemy", "alembic", "aiosqlite"]
            missing_deps = [dep for dep in required_deps if dep not in content.lower()]
            
            if not missing_deps:
                checks.append(("Dependencies", True, "All required dependencies present"))
            else:
                checks.append(("Dependencies", False, f"Missing: {missing_deps}"))
    
    # Print results
    passed = 0
    for check_name, status, message in checks:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {check_name:<20} - {message}")
        if status:
            passed += 1
    
    print(f"\n📊 Integration Validation: {passed}/{len(checks)} checks passed")
    return passed == len(checks)

def main():
    """Main validation function"""
    print("🔍 CODEBRIDGE STEPS 1 & 2 COMPREHENSIVE VALIDATION")
    print("=" * 80)
    print(f"📅 Validation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Validating against you.md requirements")
    print()
    
    # Run all validations
    validations = [
        ("Project Structure", validate_project_structure),
        ("Step 1 Implementation", validate_step1_implementation), 
        ("Step 2 Database", validate_step2_database),
        ("Integration", validate_integration)
    ]
    
    results = []
    for validation_name, validation_func in validations:
        try:
            result = validation_func()
            results.append((validation_name, result))
        except Exception as e:
            print(f"❌ {validation_name} validation failed with error: {e}")
            results.append((validation_name, False))
        
        print()  # Add spacing between validations
    
    # Final summary
    print("=" * 80)
    print("🏆 FINAL VALIDATION SUMMARY")
    print("=" * 80)
    
    all_passed = True
    for validation_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {validation_name}")
        if not passed:
            all_passed = False
    
    print(f"\n📊 Overall Result: {sum(1 for _, passed in results if passed)}/{len(results)} validations passed")
    
    if all_passed:
        print("\n🎉 SUCCESS! Both Step 1 and Step 2 are FULLY IMPLEMENTED!")
        print("✅ Project Skeleton Setup (Step 1) - COMPLETE")
        print("✅ Database Foundation (Step 2) - COMPLETE") 
        print("🚀 Ready to proceed to Step 3!")
    else:
        print(f"\n⚠️  Issues found. Please address the failed validations above.")
    
    print("=" * 80)
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
