"""
Endpoint Testing Script
======================

This script tests all endpoints once the server is running.
Run this after starting the server to validate all functionality.
"""

import requests
import json
import time
import sys

def test_endpoint(url, description, expected_status=200):
    """Test a single endpoint"""
    try:
        print(f"🔍 Testing: {description}")
        print(f"   URL: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == expected_status:
            print(f"   ✅ Status: {response.status_code}")
            
            # Try to parse JSON response
            try:
                data = response.json()
                if isinstance(data, dict):
                    if "status" in data:
                        print(f"   📊 Status: {data.get('status', 'N/A')}")
                    if "message" in data:
                        print(f"   💬 Message: {data.get('message', 'N/A')}")
                    if "version" in data:
                        print(f"   🏷️  Version: {data.get('version', 'N/A')}")
                print(f"   📝 Response: Valid JSON ({len(str(data))} chars)")
            except:
                print(f"   📝 Response: {len(response.text)} characters")
                
            return True
        else:
            print(f"   ❌ Status: {response.status_code} (expected {expected_status})")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Connection failed - is the server running?")
        return False
    except requests.exceptions.Timeout:
        print(f"   ❌ Request timeout")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_database_health():
    """Test database health endpoint specifically"""
    print(f"\n🗄️  DETAILED DATABASE HEALTH TEST")
    print("-" * 50)
    
    try:
        response = requests.get("http://localhost:3047/api/health/database", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Database health endpoint accessible")
            
            # Check database connection
            if "database" in data:
                db_info = data["database"]
                connected = db_info.get("connected", False)
                print(f"   🔌 Connected: {connected}")
                
                if "connection_info" in db_info:
                    conn_info = db_info["connection_info"]
                    print(f"   🏠 Host: {conn_info.get('host', 'N/A')}")
                    print(f"   📊 Pool size: {conn_info.get('pool_size', 'N/A')}")
                    print(f"   🔗 Checked out: {conn_info.get('checked_out_connections', 'N/A')}")
                
                if "statistics" in db_info:
                    stats = db_info["statistics"]
                    print(f"   📈 Total projects: {stats.get('total_projects', 'N/A')}")
                    print(f"   📄 Total content: {stats.get('total_content', 'N/A')}")
                
                return connected
            else:
                print("❌ No database info in response")
                return False
        else:
            print(f"❌ Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Database health test failed: {e}")
        return False

def main():
    """Main testing function"""
    print("🧪 CODEBRIDGE ENDPOINT TESTING")
    print("=" * 60)
    print(f"🕐 Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🌐 Target: http://localhost:3047")
    print()
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    # Define endpoints to test
    endpoints = [
        ("http://localhost:3047/", "Root endpoint"),
        ("http://localhost:3047/api/health/simple", "Simple health check"),
        ("http://localhost:3047/api/health", "Full health check"),
        ("http://localhost:3047/api/health/database", "Database health check"),
        ("http://localhost:3047/docs", "API documentation (Swagger)"),
        ("http://localhost:3047/redoc", "API documentation (ReDoc)"),
        ("http://localhost:3047/openapi.json", "OpenAPI schema"),
    ]
    
    # Test each endpoint
    passed = 0
    total = len(endpoints)
    
    print("📋 ENDPOINT TESTS")
    print("-" * 50)
    
    for url, description in endpoints:
        print()
        if test_endpoint(url, description):
            passed += 1
        print()
    
    # Detailed database test
    db_health = test_database_health()
    
    # Summary
    print(f"\n{'=' * 60}")
    print("🏆 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"📊 Endpoint Tests: {passed}/{total} passed")
    print(f"🗄️  Database Health: {'✅ PASSED' if db_health else '❌ FAILED'}")
    
    overall_success = (passed == total) and db_health
    
    if overall_success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print("✅ CodeBridge system is fully operational")
        print("✅ All endpoints responding correctly")
        print("✅ Database connectivity confirmed")
        print(f"\n🌐 System URLs:")
        print(f"   • Main API: http://localhost:3047/")
        print(f"   • Health Check: http://localhost:3047/api/health")
        print(f"   • Database Status: http://localhost:3047/api/health/database") 
        print(f"   • API Documentation: http://localhost:3047/docs")
        print(f"\n🚀 Ready for Step 3 development!")
    else:
        print(f"\n❌ Some tests failed:")
        if passed != total:
            print(f"   • {total - passed} endpoint(s) failed")
        if not db_health:
            print(f"   • Database health check failed")
        print("Please check the server logs and fix any issues.")
    
    print("=" * 60)
    return overall_success

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
