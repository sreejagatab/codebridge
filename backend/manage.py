#!/usr/bin/env python3
"""
Management script for CodeBridge backend
Handles database migrations, seeding, and other administrative tasks
"""

import asyncio
import sys
from pathlib import Path
import argparse
import logging

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent))

from alembic.config import Config
from alembic import command
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, test_connection, create_tables, drop_tables
from app.services.database_service import seed_database

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_migrations():
    """Run Alembic migrations to latest"""
    try:
        logger.info("Running database migrations...")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("✅ Database migrations completed successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
        return False


def rollback_migrations(revision: str = "-1"):
    """Rollback migrations to specified revision"""
    try:
        logger.info(f"Rolling back migrations to: {revision}")
        alembic_cfg = Config("alembic.ini")
        command.downgrade(alembic_cfg, revision)
        logger.info("✅ Database rollback completed successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return False


def create_migration(message: str):
    """Create a new migration"""
    try:
        logger.info(f"Creating new migration: {message}")
        alembic_cfg = Config("alembic.ini")
        command.revision(alembic_cfg, message=message, autogenerate=True)
        logger.info("✅ Migration created successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Migration creation failed: {e}")
        return False


async def test_db_connection():
    """Test database connection"""
    logger.info("Testing database connection...")
    result = await test_connection()
    if result:
        logger.info("✅ Database connection successful!")
    else:
        logger.error("❌ Database connection failed!")
    return result


def seed_db():
    """Seed database with initial data"""
    try:
        logger.info("Seeding database...")
        db = SessionLocal()
        try:
            seed_database(db)
            logger.info("✅ Database seeding completed successfully!")
            return True
        finally:
            db.close()
    except Exception as e:
        logger.error(f"❌ Database seeding failed: {e}")
        return False


def reset_db():
    """Reset database (drop and recreate tables)"""
    try:
        logger.info("Resetting database...")
        drop_tables()
        create_tables()
        logger.info("✅ Database reset completed successfully!")
        return True
    except Exception as e:
        logger.error(f"❌ Database reset failed: {e}")
        return False


async def init_db():
    """Initialize database: run migrations and seed data"""
    logger.info("Initializing database...")
    
    # Test connection first
    if not await test_db_connection():
        logger.error("❌ Cannot connect to database. Please check your database configuration.")
        return False
    
    # Run migrations
    if not run_migrations():
        logger.error("❌ Database initialization failed during migrations.")
        return False
    
    # Seed database
    if not seed_db():
        logger.error("❌ Database initialization failed during seeding.")
        return False
    
    logger.info("✅ Database initialization completed successfully!")
    return True


def main():
    """Main management function"""
    parser = argparse.ArgumentParser(description="CodeBridge Backend Management")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Migration commands
    migrate_parser = subparsers.add_parser("migrate", help="Run database migrations")
    
    rollback_parser = subparsers.add_parser("rollback", help="Rollback database migrations")
    rollback_parser.add_argument("--revision", default="-1", help="Revision to rollback to")
    
    makemigration_parser = subparsers.add_parser("makemigration", help="Create new migration")
    makemigration_parser.add_argument("message", help="Migration message")
    
    # Database commands
    subparsers.add_parser("test-db", help="Test database connection")
    subparsers.add_parser("seed", help="Seed database with initial data")
    subparsers.add_parser("reset-db", help="Reset database (drop and recreate)")
    subparsers.add_parser("init-db", help="Initialize database (migrate + seed)")
    
    args = parser.parse_args()
    
    if args.command == "migrate":
        success = run_migrations()
    elif args.command == "rollback":
        success = rollback_migrations(args.revision)
    elif args.command == "makemigration":
        success = create_migration(args.message)
    elif args.command == "test-db":
        success = asyncio.run(test_db_connection())
    elif args.command == "seed":
        success = seed_db()
    elif args.command == "reset-db":
        success = reset_db()
    elif args.command == "init-db":
        success = asyncio.run(init_db())
    else:
        parser.print_help()
        success = False
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
