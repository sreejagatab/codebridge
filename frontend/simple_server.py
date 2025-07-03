import http.server
import socketserver
import os
import webbrowser

PORT = 3045

# Change to the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(script_dir, "public")

print(f"Script directory: {script_dir}")
print(f"Public directory: {public_dir}")

if os.path.exists(public_dir):
    os.chdir(public_dir)
    print(f"✅ Changed to directory: {public_dir}")
    print(f"📁 Files in directory: {os.listdir('.')}")
else:
    print(f"❌ Public directory not found: {public_dir}")
    exit(1)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("=" * 60)
    print("🌉 CodeBridge Frontend Server")
    print("=" * 60)
    print(f"📡 Server running at: http://localhost:{PORT}")
    print(f"📁 Serving from: {os.getcwd()}")
    print("🔗 Backend API: http://localhost:3047")
    print("=" * 60)
    print("Opening browser...")
    
    try:
        webbrowser.open(f'http://localhost:{PORT}')
    except:
        print("Could not open browser automatically")
    
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
