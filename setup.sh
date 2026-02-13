#!/bin/bash

# Real Estate AI Ecosystem - Quick Setup Script

echo "🚀 Real Estate AI Ecosystem - Setup Script"
echo "=========================================="

# Check Python version
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

# Copy environment file
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys"
fi

# Create database
echo "Initializing database..."
cd backend
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: cd backend && uvicorn app.main:app --reload"
echo "3. Visit: http://localhost:8000/docs"
echo ""
