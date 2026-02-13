#!/usr/bin/env python
"""
Real Estate AI Ecosystem - Quick Start Script
"""
import os
import sys
import asyncio
import subprocess
from pathlib import Path

def setup_environment():
    """Setup environment variables"""
    print("🔧 Setting up environment...")
    
    if not Path(".env").exists():
        print("Creating .env file from template...")
        Path(".env").write_text(Path(".env.example").read_text())
        print("⚠️  Please edit .env with your API keys")
        return False
    print("✓ .env file found")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"], check=True)
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def init_database():
    """Initialize database"""
    print("🗄️  Initializing database...")
    try:
        os.chdir("backend")
        from app.database import init_db
        asyncio.run(init_db())
        os.chdir("..")
        print("✓ Database initialized")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        os.chdir("..")
        return False

def start_backend():
    """Start FastAPI backend"""
    print("🚀 Starting backend server...")
    os.chdir("backend")
    try:
        subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--reload"])
    except KeyboardInterrupt:
        print("\n👋 Backend stopped")
    finally:
        os.chdir("..")

def main():
    """Main setup flow"""
    print("╔════════════════════════════════════════╗")
    print("║  Real Estate AI Ecosystem - Quick Start║")
    print("╚════════════════════════════════════════╝")
    print()
    
    # Setup
    if not setup_environment():
        print("\n⚠️  Please fill in your API keys in .env file first")
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Initialize database
    if not init_database():
        return
    
    print()
    print("✅ Setup complete!")
    print()
    print("🌐 Opening http://localhost:8000")
    print()
    
    # Start backend
    start_backend()

if __name__ == "__main__":
    main()
