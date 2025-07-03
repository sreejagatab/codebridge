import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

try:
    from app.main import app
    from app.core.config import settings
    print(f"SUCCESS: FastAPI app loaded - {settings.APP_NAME} v{settings.VERSION} on port {settings.PORT}")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)

try:
    from app.core.database import create_tables, SessionLocal
    create_tables()
    print("SUCCESS: Database tables created")
except Exception as e:
    print(f"ERROR: Database setup failed - {e}")
    sys.exit(1)

try:
    from app.services.database_service import ProjectService
    db = SessionLocal()
    projects = ProjectService.get_projects(db, limit=5)
    print(f"SUCCESS: Database operations working - found {len(projects)} projects")
    db.close()
except Exception as e:
    print(f"ERROR: Database operations failed - {e}")
    sys.exit(1)

print("ALL TESTS PASSED - System is ready!")
