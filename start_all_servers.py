#!/usr/bin/env python3
"""
Single script to start both API and Dashboard servers
Runs uvicorn (API) and HTTP server (dashboard) in parallel
"""
import subprocess
import sys
import time
import signal
import os
from pathlib import Path

import socket

# ANSI color codes
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

processes = []

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def kill_process_on_port(port):
    """Attempts to find and kill process on a specific port (Windows/Linux)"""
    try:
        if sys.platform == 'win32':
            # Windows: Find PID and kill
            cmd = f"netstat -ano | findstr :{port}"
            output = subprocess.check_output(cmd, shell=True).decode()
            for line in output.splitlines():
                parts = line.split()
                if str(port) in parts[1]: # Check local address matches port
                    pid = parts[-1]
                    print(f"{YELLOW}⚠️ Killing process {pid} on port {port}...{RESET}")
                    subprocess.run(f"taskkill /F /PID {pid}", shell=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        else:
            # Linux/Mac: Use lsof or fuser
            subprocess.run(f"fuser -k {port}/tcp", shell=True, stderr=subprocess.DEVNULL)
    except Exception:
        pass

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n{YELLOW}🛑 Shutting down servers...{RESET}")
    for process in processes:
        process.terminate()
    sys.exit(0)

def main():
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    print(f"{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{GREEN}🚀 Starting GitHub Gists API Dashboard System{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
    
    # Check if running from correct directory
    if not os.path.exists('app/main.py'):
        print(f"{RED}❌ Error: Must run from project root directory{RESET}")
        print(f"{YELLOW}   (Directory containing app/ folder){RESET}")
        sys.exit(1)
    
    if not os.path.exists('performance-dashboard.html'):
        print(f"{RED}❌ Error: performance-dashboard.html not found{RESET}")
        sys.exit(1)
    
    # Check and cleanup ports
    for port, name in [(8080, "API"), (3000, "Dashboard")]:
        if is_port_in_use(port):
            print(f"{YELLOW}⚠️ Port {port} ({name}) is in use. Cleaning up...{RESET}")
            kill_process_on_port(port)
            time.sleep(1) # Wait for cleanup
    
    try:
        # Start API server (uvicorn) 
        print(f"{BLUE}📡 Starting API Server on http://localhost:8080{RESET}")
        api_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.main:app", 
             "--host", "0.0.0.0", "--port", "8080"],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        processes.append(api_process)
        print(f"{GREEN}✓ API Server started (PID: {api_process.pid}){RESET}\n")
        
        # Wait a moment for API to start
        time.sleep(3)
        
        # Start Dashboard server
        print(f"{BLUE}🎨 Starting Dashboard Server on http://localhost:3000{RESET}")
        dashboard_process = subprocess.Popen(
            [sys.executable, "serve_dashboard.py"],
            creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == 'win32' else 0
        )
        processes.append(dashboard_process)
        print(f"{GREEN}✓ Dashboard Server started (PID: {dashboard_process.pid}){RESET}\n")
        
        # Wait a moment for dashboard to start
        time.sleep(2)
        
        print(f"{BOLD}{GREEN}{'='*70}{RESET}")
        print(f"{BOLD}{GREEN}✅ All servers are running!{RESET}")
        print(f"{BOLD}{GREEN}{'='*70}{RESET}\n")
        
        print(f"{BOLD}🌐 Access URLs:{RESET}")
        print(f"  {BLUE}API:{RESET}           {BOLD}http://localhost:8080{RESET}")
        print(f"  {BLUE}Dashboard:{RESET}     {BOLD}http://localhost:3000/performance-dashboard.html{RESET}")
        print(f"  {BLUE}Health Check:{RESET}  {BOLD}http://localhost:8080/health{RESET}")
        print(f"  {BLUE}Metrics:{RESET}       {BOLD}http://localhost:8080/metrics{RESET}\n")
        
        print(f"{YELLOW}💡 Quick Test:{RESET}")
        print(f"   curl http://localhost:8080/octocat\n")
        
        print(f"{YELLOW}🛑 Press Ctrl+C to stop all servers{RESET}\n")
        print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")
        
        # Keep the script running and monitor processes
        while True:
            # Check if any process has died
            for i, process in enumerate(processes):
                if process.poll() is not None:
                    print(f"{RED}❌ Server {i+1} died unexpectedly!{RESET}")
                    # Kill all other processes
                    for p in processes:
                        if p.poll() is None:
                            p.terminate()
                    sys.exit(1)
            
            time.sleep(1)
            
    except Exception as e:
        print(f"{RED}❌ Error: {e}{RESET}")
        for process in processes:
            process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()
