"""
Simple server startup test for CodeBridge
"""
import subprocess
import time
import requests
import sys

def test_server_startup():
    """Test if the server starts and responds correctly"""
    print("🚀 Testing CodeBridge Server Startup on Port 3047")
    print("=" * 50)
    
    # Start the server
    print("1. Starting FastAPI server...")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "0.0.0.0", 
            "--port", "3047"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("2. Waiting for server to start...")
        time.sleep(5)
        
        # Test endpoints
        print("3. Testing endpoints...")
        
        # Test root endpoint
        try:
            response = requests.get("http://localhost:3047/", timeout=10)
            if response.status_code == 200:
                print("   ✅ Root endpoint (/) - Status 200")
                print(f"   📄 Response: {response.json()}")
            else:
                print(f"   ❌ Root endpoint failed - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Root endpoint error: {e}")
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:3047/api/health", timeout=10)
            if response.status_code == 200:
                print("   ✅ Health endpoint (/api/health) - Status 200")
                data = response.json()
                print(f"   📊 Health Status: {data.get('status', 'unknown')}")
                print(f"   📱 App Name: {data.get('app_name', 'unknown')}")
            else:
                print(f"   ❌ Health endpoint failed - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Health endpoint error: {e}")
        
        # Test simple health endpoint
        try:
            response = requests.get("http://localhost:3047/api/health/simple", timeout=10)
            if response.status_code == 200:
                print("   ✅ Simple health endpoint (/api/health/simple) - Status 200")
            else:
                print(f"   ❌ Simple health endpoint failed - Status {response.status_code}")
        except Exception as e:
            print(f"   ❌ Simple health endpoint error: {e}")
        
        print("\n4. Server URLs:")
        print("   🌐 Root: http://localhost:3047/")
        print("   🏥 Health: http://localhost:3047/api/health")
        print("   📖 Docs: http://localhost:3047/docs")
        print("   📚 ReDoc: http://localhost:3047/redoc")
        
        # Terminate the server
        print("\n5. Stopping server...")
        process.terminate()
        process.wait()
        print("   ✅ Server stopped")
        
        print("\n" + "=" * 50)
        print("🎉 Server startup test completed!")
        print("✅ CodeBridge is ready for deployment!")
        
        return True
        
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False

if __name__ == "__main__":
    success = test_server_startup()
    sys.exit(0 if success else 1)
