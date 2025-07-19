#!/usr/bin/env python3
"""
Production deployment script for swipekarbhai
Runs both frontend and backend together
"""

import subprocess
import os
import sys
import time
from threading import Thread

def run_frontend():
    """Run frontend server on port 8080"""
    print("🌐 Starting Frontend Server...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "-m", "http.server", "8080"])

def run_backend():
    """Run backend server on port 5001"""
    print("⚙️  Starting Backend API Server...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.run([sys.executable, "server.py"])

def main():
    """Start both servers"""
    print("🚀 Starting swipekarbhai Full Stack Application")
    print("=" * 50)
    print("Frontend: http://localhost:8080")
    print("Backend API: http://localhost:5001")
    print("=" * 50)
    
    # Start backend in background
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Give backend time to start
    time.sleep(2)
    
    # Start frontend
    run_frontend()

if __name__ == "__main__":
    main()
