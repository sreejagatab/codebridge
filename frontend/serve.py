#!/usr/bin/env python3
"""
Simple HTTP server for CodeBridge frontend
Serves static files from the public directory on port 3045
"""

import http.server
import socketserver
import os
import sys

# Change to the frontend/public directory
frontend_dir = os.path.dirname(os.path.abspath(__file__))
public_dir = os.path.join(frontend_dir, "public")

if os.path.exists(public_dir):
    os.chdir(public_dir)
    print(f"✅ Changed to directory: {public_dir}")
else:
    print(f"❌ Public directory not found: {public_dir}")
    sys.exit(1)

PORT = 3045

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 50)
    print("🌉 CodeBridge Frontend Server")
    print("=" * 50)
    print(f"📡 Server running on: http://localhost:{PORT}")
    print(f"📁 Serving files from: {os.getcwd()}")
    print("🔗 Backend API: http://localhost:3047")
    print("=" * 50)
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        httpd.shutdown()
