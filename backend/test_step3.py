"""
Step 3 Testing Script: Basic API Framework
==========================================

This script tests all the new API endpoints introduced in Step 3:
- Authentication endpoints
- Project CRUD operations
- Content CRUD operations
- Rate limiting
- Request validation
- API documentation
"""

import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:3047"
AUTH_HEADERS = {}

def log_test(test_name, success, details=""):
    """Log test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} {test_name}")
    if details:
        print(f"    {details}")

def test_authentication():
    """Test authentication endpoints"""
    print("\n🔐 TESTING AUTHENTICATION")
    print("=" * 50)
    
    # Test login with valid credentials
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", data={
            "username": "admin",
            "password": "admin123"
        })
        
        if response.status_code == 200:
            token_data = response.json()
            AUTH_HEADERS["Authorization"] = f"Bearer {token_data['access_token']}"
            log_test("Admin login", True, f"Token received, expires in {token_data['expires_in']} seconds")
        else:
            log_test("Admin login", False, f"Status: {response.status_code}")
            return False
    except Exception as e:
        log_test("Admin login", False, f"Error: {e}")
        return False
    
    # Test /me endpoint
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=AUTH_HEADERS)
        if response.status_code == 200:
            user_data = response.json()
            log_test("Get user info", True, f"User: {user_data['data']['username']}, Permissions: {user_data['data']['permissions']}")
        else:
            log_test("Get user info", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Get user info", False, f"Error: {e}")
    
    # Test invalid credentials
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", data={
            "username": "invalid",
            "password": "wrong"
        })
        
        if response.status_code == 401:
            log_test("Invalid login rejection", True, "Correctly rejected invalid credentials")
        else:
            log_test("Invalid login rejection", False, f"Expected 401, got {response.status_code}")
    except Exception as e:
        log_test("Invalid login rejection", False, f"Error: {e}")
    
    return True

def test_projects_api():
    """Test project CRUD operations"""
    print("\n📁 TESTING PROJECTS API")
    print("=" * 50)
    
    # Test creating a project
    test_project = {
        "platform": "github",
        "url": "https://github.com/test/test-repo",
        "name": "Test Repository",
        "description": "A test repository for API testing",
        "stars": 42,
        "language": "Python",
        "topics": ["api", "testing", "fastapi"],
        "quality_score": 8.5,
        "status": "discovered"
    }
    
    project_id = None
    try:
        response = requests.post(f"{BASE_URL}/api/projects", 
                               json=test_project, 
                               headers=AUTH_HEADERS)
        
        if response.status_code == 201:
            project_data = response.json()
            project_id = project_data['data']['id']
            log_test("Create project", True, f"Created project ID: {project_id}")
        else:
            log_test("Create project", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        log_test("Create project", False, f"Error: {e}")
        return
    
    # Test listing projects
    try:
        response = requests.get(f"{BASE_URL}/api/projects")
        if response.status_code == 200:
            projects_data = response.json()
            log_test("List projects", True, f"Retrieved {len(projects_data['data'])} projects")
        else:
            log_test("List projects", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("List projects", False, f"Error: {e}")
    
    # Test getting specific project
    if project_id:
        try:
            response = requests.get(f"{BASE_URL}/api/projects/{project_id}")
            if response.status_code == 200:
                project_data = response.json()
                log_test("Get project details", True, f"Retrieved project: {project_data['data']['name']}")
            else:
                log_test("Get project details", False, f"Status: {response.status_code}")
        except Exception as e:
            log_test("Get project details", False, f"Error: {e}")
    
    # Test updating project
    if project_id:
        try:
            update_data = {"stars": 100, "status": "analyzed"}
            response = requests.put(f"{BASE_URL}/api/projects/{project_id}", 
                                  json=update_data, 
                                  headers=AUTH_HEADERS)
            
            if response.status_code == 200:
                log_test("Update project", True, "Project updated successfully")
            else:
                log_test("Update project", False, f"Status: {response.status_code}")
        except Exception as e:
            log_test("Update project", False, f"Error: {e}")
    
    # Test project filtering
    try:
        response = requests.get(f"{BASE_URL}/api/projects?platform=github&limit=5")
        if response.status_code == 200:
            projects_data = response.json()
            log_test("Filter projects", True, f"Filtered results: {len(projects_data['data'])} projects")
        else:
            log_test("Filter projects", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Filter projects", False, f"Error: {e}")
    
    return project_id

def test_content_api(project_id):
    """Test content CRUD operations"""
    print("\n📝 TESTING CONTENT API")
    print("=" * 50)
    
    if not project_id:
        log_test("Content API tests", False, "No project ID available")
        return
    
    # Test creating content
    test_content = {
        "project_id": project_id,
        "content_type": "blog",
        "title": "Getting Started with Test Repository",
        "slug": "getting-started-test-repo",
        "raw_content": "# Test Repository\n\nThis is a sample README content...",
        "meta_description": "Learn how to get started with the test repository",
        "tags": ["tutorial", "getting-started", "python"],
        "status": "draft"
    }
    
    content_id = None
    try:
        response = requests.post(f"{BASE_URL}/api/content", 
                               json=test_content, 
                               headers=AUTH_HEADERS)
        
        if response.status_code == 201:
            content_data = response.json()
            content_id = content_data['data']['id']
            log_test("Create content", True, f"Created content ID: {content_id}")
        else:
            log_test("Create content", False, f"Status: {response.status_code}, Response: {response.text}")
            return
    except Exception as e:
        log_test("Create content", False, f"Error: {e}")
        return
    
    # Test listing content
    try:
        response = requests.get(f"{BASE_URL}/api/content")
        if response.status_code == 200:
            content_data = response.json()
            log_test("List content", True, f"Retrieved {len(content_data['data'])} content items")
        else:
            log_test("List content", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("List content", False, f"Error: {e}")
    
    # Test getting content by ID
    if content_id:
        try:
            response = requests.get(f"{BASE_URL}/api/content/{content_id}?include_raw=true")
            if response.status_code == 200:
                content_data = response.json()
                log_test("Get content details", True, f"Retrieved content: {content_data['data']['title']}")
            else:
                log_test("Get content details", False, f"Status: {response.status_code}")
        except Exception as e:
            log_test("Get content details", False, f"Error: {e}")
    
    # Test getting content by slug
    try:
        response = requests.get(f"{BASE_URL}/api/content/by-slug/getting-started-test-repo")
        if response.status_code == 200:
            content_data = response.json()
            log_test("Get content by slug", True, f"Retrieved content via slug")
        else:
            log_test("Get content by slug", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Get content by slug", False, f"Error: {e}")
    
    # Test content filtering
    try:
        response = requests.get(f"{BASE_URL}/api/content?project_id={project_id}&content_type=blog")
        if response.status_code == 200:
            content_data = response.json()
            log_test("Filter content", True, f"Filtered results: {len(content_data['data'])} items")
        else:
            log_test("Filter content", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Filter content", False, f"Error: {e}")

def test_request_validation():
    """Test request validation"""
    print("\n✅ TESTING REQUEST VALIDATION")
    print("=" * 50)
    
    # Test invalid project data
    try:
        invalid_project = {
            "platform": "invalid_platform",  # Should be rejected
            "url": "not-a-url",  # Should be rejected
            "name": "",  # Should be rejected (empty)
        }
        
        response = requests.post(f"{BASE_URL}/api/projects", 
                               json=invalid_project, 
                               headers=AUTH_HEADERS)
        
        if response.status_code == 422:
            log_test("Invalid project validation", True, "Correctly rejected invalid project data")
        else:
            log_test("Invalid project validation", False, f"Expected 422, got {response.status_code}")
    except Exception as e:
        log_test("Invalid project validation", False, f"Error: {e}")
    
    # Test invalid content data
    try:
        invalid_content = {
            "project_id": 99999,  # Non-existent project
            "content_type": "",  # Empty
            "title": "",  # Empty
            "slug": "Invalid Slug!",  # Invalid characters
            "raw_content": ""  # Empty
        }
        
        response = requests.post(f"{BASE_URL}/api/content", 
                               json=invalid_content, 
                               headers=AUTH_HEADERS)
        
        if response.status_code in [422, 404]:
            log_test("Invalid content validation", True, "Correctly rejected invalid content data")
        else:
            log_test("Invalid content validation", False, f"Expected 422/404, got {response.status_code}")
    except Exception as e:
        log_test("Invalid content validation", False, f"Error: {e}")

def test_authorization():
    """Test authorization and permissions"""
    print("\n🔒 TESTING AUTHORIZATION")
    print("=" * 50)
    
    # Test accessing protected endpoint without token
    try:
        response = requests.post(f"{BASE_URL}/api/projects", json={
            "platform": "github",
            "url": "https://github.com/test/unauthorized",
            "name": "Unauthorized Test"
        })
        
        if response.status_code == 401:
            log_test("Unauthorized access rejection", True, "Correctly rejected request without token")
        else:
            log_test("Unauthorized access rejection", False, f"Expected 401, got {response.status_code}")
    except Exception as e:
        log_test("Unauthorized access rejection", False, f"Error: {e}")
    
    # Test with invalid token
    try:
        invalid_headers = {"Authorization": "Bearer invalid.token.here"}
        response = requests.post(f"{BASE_URL}/api/projects", 
                               json={"platform": "github", "url": "https://github.com/test/invalid", "name": "Invalid Token Test"},
                               headers=invalid_headers)
        
        if response.status_code == 401:
            log_test("Invalid token rejection", True, "Correctly rejected invalid token")
        else:
            log_test("Invalid token rejection", False, f"Expected 401, got {response.status_code}")
    except Exception as e:
        log_test("Invalid token rejection", False, f"Error: {e}")

def test_rate_limiting():
    """Test rate limiting functionality"""
    print("\n⏱️ TESTING RATE LIMITING")
    print("=" * 50)
    
    # Make multiple rapid requests to trigger rate limiting
    success_count = 0
    rate_limited = False
    
    print("Making 65 rapid requests to test rate limiting...")
    
    for i in range(65):
        try:
            response = requests.get(f"{BASE_URL}/api/projects?limit=1")
            if response.status_code == 429:
                rate_limited = True
                break
            elif response.status_code == 200:
                success_count += 1
        except Exception as e:
            break
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.01)
    
    if rate_limited:
        log_test("Rate limiting", True, f"Rate limit triggered after {success_count} requests")
    else:
        log_test("Rate limiting", False, f"Made {success_count} requests without hitting rate limit")

def test_api_documentation():
    """Test API documentation availability"""
    print("\n📚 TESTING API DOCUMENTATION")
    print("=" * 50)
    
    # Test OpenAPI schema
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            schema = response.json()
            log_test("OpenAPI schema", True, f"Schema available with {len(schema.get('paths', {}))} endpoints")
        else:
            log_test("OpenAPI schema", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("OpenAPI schema", False, f"Error: {e}")
    
    # Test Swagger UI
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code == 200:
            log_test("Swagger UI", True, "Documentation UI accessible")
        else:
            log_test("Swagger UI", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("Swagger UI", False, f"Error: {e}")
    
    # Test ReDoc
    try:
        response = requests.get(f"{BASE_URL}/redoc")
        if response.status_code == 200:
            log_test("ReDoc UI", True, "ReDoc documentation accessible")
        else:
            log_test("ReDoc UI", False, f"Status: {response.status_code}")
    except Exception as e:
        log_test("ReDoc UI", False, f"Error: {e}")

def main():
    """Run all Step 3 tests"""
    print("🧪 CODEBRIDGE STEP 3 API TESTING")
    print("=" * 60)
    print(f"Testing API at: {BASE_URL}")
    print(f"Started at: {datetime.now().isoformat()}")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Is it running on port 3047?")
        print("   Run: python -m uvicorn app.main:app --host 0.0.0.0 --port 3047")
        sys.exit(1)
    
    print("✅ Server is running and responding")
    
    # Run tests
    auth_success = test_authentication()
    if not auth_success:
        print("\n❌ Authentication tests failed - cannot proceed with protected endpoint tests")
        sys.exit(1)
    
    project_id = test_projects_api()
    test_content_api(project_id)
    test_request_validation()
    test_authorization()
    test_rate_limiting()
    test_api_documentation()
    
    print("\n" + "=" * 60)
    print("🎉 STEP 3 TESTING COMPLETED")
    print("=" * 60)
    print("✅ All Step 3 requirements tested:")
    print("   • RESTful API endpoints")
    print("   • Request/response validation with Pydantic")
    print("   • JWT Authentication middleware")
    print("   • Rate limiting")
    print("   • API documentation with OpenAPI/Swagger")
    print()
    print("🌐 API Documentation available at:")
    print(f"   • Swagger UI: {BASE_URL}/docs")
    print(f"   • ReDoc: {BASE_URL}/redoc")
    print()
    print("🔐 Demo credentials for testing:")
    print("   • Username: admin, Password: admin123")
    print("   • Username: user, Password: user123")

if __name__ == "__main__":
    main()
