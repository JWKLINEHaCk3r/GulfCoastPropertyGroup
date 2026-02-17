#!/bin/bash
set -e

echo "🚀 Starting Gulf Coast Property Group - Level 100 Platform"
echo "================================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ==================== FRONTEND BUILD ====================
echo -e "${BLUE}📦 Building Frontend...${NC}"
cd frontend

# Install dependencies
echo "Installing frontend dependencies..."
npm install --production

# Build for production
echo "Building production frontend..."
npm run build

# Move to backend static folder for serving
echo "Preparing frontend assets..."
cd ..
mkdir -p backend/static
cp -r frontend/dist/* backend/static/

echo -e "${GREEN}✅ Frontend built successfully${NC}"

# ==================== BACKEND SETUP ====================
echo -e "${BLUE}🔧 Setting up Backend...${NC}"
cd backend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Set production environment
export ENVIRONMENT=production
export DEBUG=false

# Database initialization (if needed)
if [[ -n "${DATABASE_URL}" ]]; then
  echo "Running database migrations..."
  alembic upgrade head || true
fi

echo -e "${GREEN}✅ Backend setup complete${NC}"

# ==================== START APPLICATION ====================
echo -e "${BLUE}🌟 Starting Application...${NC}"

# Determine port (Railway sets PORT env variable)
PORT=${PORT:-8000}
WORKERS=${WORKERS:-4}

echo "Starting Uvicorn server on port $PORT with $WORKERS workers..."
echo "================================================================"

# Start FastAPI with Uvicorn
exec uvicorn app.main:app \
  --host 0.0.0.0 \
  --port $PORT \
  --workers $WORKERS \
  --access-log
