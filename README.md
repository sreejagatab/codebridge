# CodeBridge - README-to-Blog Automation Platform

**"Bridging the Gap Between Code and Community"**

A production-ready, full-stack platform that transforms README files from GitHub, Hugging Face, GitLab, and other platforms into engaging blog posts using AI enhancement. Built with FastAPI, React, and modern development practices following a 100-step phased development approach.

## 🎯 Project Status

✅ **Step 1 Complete**: Project Skeleton Setup  
✅ **Step 2 Complete**: Database Foundation  
🔄 **Step 3**: Next Phase (Ready to Begin)

## 🏗️ Architecture Overview

```
codebridge/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── core/              # Core configuration and setup
│   │   │   ├── config.py      # Settings and configuration
│   │   │   ├── database.py    # Database connection & pooling
│   │   │   └── logging_config.py # Structured JSON logging
│   │   ├── api/               # API routes
│   │   │   └── health.py      # Health check endpoints (with DB monitoring)
│   │   ├── models/            # SQLAlchemy database models
│   │   │   └── database.py    # Project and Content models
│   │   ├── services/          # Business logic
│   │   │   └── database_service.py # CRUD operations & seeding
│   │   └── utils/             # Utility functions
│   ├── alembic/               # Database migrations
│   │   ├── versions/          # Migration files
│   │   ├── env.py            # Alembic environment
│   │   └── script.py.mako    # Migration template
│   ├── tests/                 # Test suite
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   ├── docker-compose.yml    # Docker Compose setup (with PostgreSQL)
│   ├── alembic.ini           # Database migration configuration
│   ├── manage.py             # Database management CLI
│   └── codebridge.db         # SQLite database file
├── frontend/                  # Static HTML frontend
│   ├── public/
│   │   └── index.html        # Main frontend page
│   ├── simple_server.py      # Development HTTP server
│   └── start.bat            # Frontend startup script
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
└── README.md                  # This file
```

## 🚀 Features

### ✅ Core Foundation (Steps 1-2)
- **FastAPI Application**: Modern, fast web framework with automatic API documentation
- **Database Foundation**: SQLAlchemy models, Alembic migrations, connection pooling
- **Health Monitoring**: Comprehensive health endpoints with database connectivity checks
- **Structured Logging**: JSON-formatted logs with proper error handling
- **Environment Configuration**: Flexible configuration management with Pydantic
- **CORS Support**: Configurable cross-origin resource sharing
- **Error Handling**: Global error handling middleware with proper logging
- **Docker Support**: Full containerization with Docker and Docker Compose
- **Testing**: Comprehensive test suites for validation

### 🗄️ Database System
- **Models**: Project and Content entities with relationships
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Connection Pooling**: Optimized database connection management
- **Migrations**: Alembic-based schema versioning and updates
- **Seeding**: Sample data for development and testing
- **Health Checks**: Real-time database connectivity and statistics

### 🔧 Development Tools
- **Management CLI**: Database operations, migrations, seeding
- **Validation Scripts**: Step-by-step verification tools
- **Startup Scripts**: Easy server and database initialization
- **Testing Framework**: Comprehensive validation suites

## 🏃‍♂️ Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd codebridge/backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
# Option 1: Automatic initialization
python manage.py init-db

# Option 2: Step by step
python manage.py migrate
python manage.py seed
```

### 4. Start the Backend Server
```bash
# Using startup script (recommended)
start_server.bat

# Or manually
python -m uvicorn app.main:app --host 0.0.0.0 --port 3047 --reload
```

### 5. Start the Frontend (Optional)
```bash
cd ../frontend
start.bat
```

### 6. Verify Installation
```bash
# Backend validation
python validate_steps_1_2.py

# Database validation  
python demo_step2.py

# Test connection
curl http://localhost:3047/api/health/database
```

## 🌐 API Endpoints

### Core Endpoints
- **Root**: `GET /` - Welcome message and app info
- **API Documentation**: `GET /docs` - Interactive Swagger UI
- **API Docs (ReDoc)**: `GET /redoc` - Alternative API documentation

### Health Monitoring
- **Health Check**: `GET /api/health` - Detailed health with system metrics
- **Database Health**: `GET /api/health/database` - Database connectivity and stats
- **Simple Health**: `GET /api/health/simple` - Basic health status

### Database Endpoints (Available via health monitoring)
- Database connection status
- Table statistics (projects, content)
- Connection pool information
- Performance metrics

## 🗄️ Database Schema

### Projects Table
```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    platform VARCHAR(50) NOT NULL,
    url TEXT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    stars INTEGER DEFAULT 0,
    language VARCHAR(50),
    topics TEXT,  -- JSON array
    quality_score DECIMAL(3,2),
    scraped_at TIMESTAMP DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'discovered'
);
```

### Content Table
```sql
CREATE TABLE content (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id),
    content_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    raw_content TEXT NOT NULL,
    enhanced_content TEXT,
    meta_description VARCHAR(160),
    tags TEXT,  -- JSON array
    status VARCHAR(20) DEFAULT 'draft',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 🧪 Testing

### Run All Validation
```bash
# Comprehensive Steps 1-2 validation
python validate_steps_1_2.py

# Database-specific validation
python demo_step2.py

# Original test suites
pytest
```

### Database Testing
```bash
# Test database connection
python manage.py test-db

# Full database workflow
python manage.py init-db
```

### Health Check Testing
```bash
# Test health endpoints
curl http://localhost:3047/api/health
curl http://localhost:3047/api/health/database
curl http://localhost:3047/api/health/simple
```

## ⚙️ Configuration

### Environment Variables
```env
# Application Configuration
APP_NAME=CodeBridge
VERSION=0.1.0
DEBUG=true
HOST=0.0.0.0
PORT=3047

# Database Configuration
DATABASE_URL=sqlite:///./codebridge.db
ASYNC_DATABASE_URL=sqlite+aiosqlite:///./codebridge.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=["*"]
```

### Database Management
```bash
# Available commands via manage.py
python manage.py migrate       # Run migrations
python manage.py rollback      # Rollback migrations
python manage.py seed          # Seed database
python manage.py test-db       # Test connection
python manage.py init-db       # Full initialization
python manage.py reset-db      # Reset database
```

## 📊 Logging & Monitoring

### Structured JSON Logging
```json
{
  "timestamp": "2025-07-03T10:30:00.123456",
  "level": "INFO",
  "logger": "app.main",
  "message": "Request completed",
  "method": "GET",
  "url": "http://localhost:3047/api/health/database",
  "status_code": 200,
  "process_time": 0.0234,
  "database_connected": true
}
```

### Health Monitoring Features
- **Application Status**: Version, environment, uptime
- **System Metrics**: CPU, memory, disk usage
- **Database Status**: Connectivity, pool stats, table counts
- **Performance**: Response times, error rates

## 🐳 Docker Deployment

### Backend with Database
```bash
# Start with PostgreSQL (production)
docker-compose up -d

# Backend only (development)
docker build -t codebridge-backend .
docker run -p 3047:3047 codebridge-backend
```

### Environment Switching
- **Development**: SQLite database (default)
- **Production**: PostgreSQL via Docker Compose
- **Testing**: In-memory SQLite

## 🔧 Development Workflow

### Code Quality
```bash
# Format code
black app/
isort app/

# Lint code
flake8 app/

# Type checking
mypy app/
```

### Database Development
```bash
# Create new migration
python manage.py makemigration "description"

# Apply migrations
python manage.py migrate

# Rollback if needed
python manage.py rollback --revision -1
```

### Testing Development
```bash
# Run specific test categories
pytest tests/test_step1.py      # Step 1 validation
pytest tests/test_step2.py      # Step 2 validation
pytest tests/test_deployment.py # Deployment tests
```

## 📈 Development Phases

### ✅ Phase 1: Production-Ready Foundation
- **Step 1**: ✅ Project Skeleton Setup
  - FastAPI application structure
  - Environment configuration
  - Logging and error handling
  - Health check endpoints
  - Docker containerization

- **Step 2**: ✅ Database Foundation
  - SQLAlchemy models (Projects, Content)
  - Alembic migration system
  - Connection pooling
  - CRUD operations
  - Database seeding

### 🔄 Phase 2: Core Features (Next)
- **Step 3**: API Foundation
- **Step 4**: Content Scraping
- **Step 5**: AI Integration
- **And more...** (following 100-step plan)

## 🎯 Validation Checklist

### Step 1 Requirements ✅
- [x] FastAPI application with proper project structure
- [x] Environment configuration management
- [x] Logging setup with structured JSON logs
- [x] Error handling middleware
- [x] CORS configuration
- [x] Docker containerization
- [x] Basic health check endpoint

### Step 2 Requirements ✅
- [x] Database connects successfully
- [x] All tables created with correct schema
- [x] Migrations run without errors
- [x] Basic CRUD operations work
- [x] Connection pooling configured

### Integration ✅
- [x] Health endpoints include database monitoring
- [x] All routers properly integrated
- [x] Configuration includes database settings
- [x] All dependencies present in requirements.txt

## 🚀 Getting Started Commands

```bash
# Quick start - Backend only
cd backend
start_server.bat

# Full stack start
start_fullstack.bat

# Database management
manage_db.bat

# Validation
python validate_steps_1_2.py
```

## 📚 Documentation

- **API Docs**: http://localhost:3047/docs
- **Health Dashboard**: http://localhost:3047/api/health
- **Database Health**: http://localhost:3047/api/health/database
- **Frontend**: http://localhost:3045 (when running)

## 🤝 Contributing

1. Follow the 100-step development plan
2. Ensure all tests pass before committing
3. Update documentation for new features
4. Follow code quality standards (black, isort, flake8)
5. Add appropriate logging and health checks

## 📄 License

MIT License - see LICENSE file for details

---

**CodeBridge** - Transforming code documentation into engaging community content through AI-powered automation.

## Project Structure

```
codebridge/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI app entry point
│   │   ├── core/              # Core configuration and setup
│   │   │   ├── config.py      # Settings and configuration
│   │   │   └── logging_config.py # Structured JSON logging
│   │   ├── api/               # API routes
│   │   │   └── health.py      # Health check endpoints
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Test suite
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile            # Docker configuration
│   ├── docker-compose.yml    # Docker Compose setup
│   └── .env.example          # Environment variables template
├── frontend/                  # Frontend application (Next.js)
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── docs/                      # Documentation
├── scripts/                   # Utility scripts
└── README.md                  # This file
```

## Features

✅ **FastAPI Application**: Modern, fast web framework with automatic API documentation  
✅ **Structured Logging**: JSON-formatted logs with proper error handling  
✅ **Health Check Endpoints**: Comprehensive health monitoring with system metrics  
✅ **Environment Configuration**: Flexible configuration management with Pydantic  
✅ **CORS Support**: Configurable cross-origin resource sharing  
✅ **Error Handling**: Global error handling middleware with proper logging  
✅ **Docker Support**: Full containerization with Docker and Docker Compose  
✅ **Testing**: Pytest setup with test client for API testing  

## Quick Start

### 1. Clone and Setup
```bash
cd codebridge/backend
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
# Development mode
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python -m app.main
```

### 4. Using Docker
```bash
# Build and run with Docker Compose
docker-compose up --build

# Or build and run manually
docker build -t codebridge-backend .
docker run -p 8000:8000 codebridge-backend
```

## API Endpoints

- **Root**: `GET /` - Welcome message and app info
- **Health Check**: `GET /api/health` - Detailed health information with system metrics
- **Simple Health**: `GET /api/health/simple` - Basic health status
- **API Documentation**: `GET /docs` - Interactive Swagger UI (development only)
- **API Docs (ReDoc)**: `GET /redoc` - Alternative API documentation (development only)

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_health.py
```

## Configuration

The application uses environment variables for configuration. Copy `.env.example` to `.env` and modify as needed:

```env
# Application Configuration
APP_NAME=CodeBridge
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
SECRET_KEY=your-secret-key-here
```

## Logging

The application uses structured JSON logging by default. Logs include:

- Timestamp (UTC)
- Log level
- Logger name
- Message
- Module, function, and line information
- Request details (method, URL, status code, processing time)
- Error information with stack traces

Example log entry:
```json
{
  "timestamp": "2025-07-03T10:30:00.123456",
  "level": "INFO", 
  "logger": "app.main",
  "message": "Request completed",
  "method": "GET",
  "url": "http://localhost:8000/api/health",
  "status_code": 200,
  "process_time": 0.0234
}
```

## Health Monitoring

The health endpoints provide comprehensive application monitoring:

- **Application Status**: Running status and version
- **System Information**: Platform, architecture, hostname
- **Performance Metrics**: CPU usage, memory consumption
- **Timestamp**: Current UTC time

## Development

### Code Quality
```bash
# Format code
black app/

# Sort imports
isort app/

# Lint code
flake8 app/
```

### Project Status
🟢 **Step 1 Complete**: Project skeleton with FastAPI, logging, health checks, and Docker support

## Next Steps

- [ ] Database integration
- [ ] Authentication and authorization
- [ ] API rate limiting
- [ ] Advanced monitoring and metrics
- [ ] Frontend implementation
- [ ] CI/CD pipeline
- [ ] Production deployment configuration

## License

MIT License
