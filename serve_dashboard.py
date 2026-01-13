#!/usr/bin/env python3
"""
HTML Dashboard Server
Serves the interactive performance dashboard with CORS enabled.
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def run_server(port=3000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, CORSRequestHandler)
    
    print("\n" + "="*70)
    print("  🚀 GitHub Gists API - Performance Dashboard")
    print("="*70)
    print(f"\n  Dashboard URL: http://localhost:{port}/performance-dashboard.html")
    print(f"\n  Make sure your API is running:")
    print(f"    - Localhost: http://localhost:8080")
    print(f"    - Production: https://gists.kishore.local")
    print(f"\n  Press Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()

if __name__ == '__main__':
    port = 3000
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    run_server(port)
