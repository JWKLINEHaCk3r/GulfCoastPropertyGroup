#!/bin/bash
# Netlify Deploy Script
# Run this script to prepare and deploy to Netlify

set -e  # Exit on error

echo "================================"
echo "Real Estate Platform - Netlify Deploy Script"
echo "================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "Download from: https://nodejs.org/"
    exit 1
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version must be 18 or higher. Current: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed."
    exit 1
fi

echo "✅ npm $(npm -v) detected"
echo ""

# Change to frontend directory
if [ ! -d "frontend" ]; then
    echo "❌ 'frontend' directory not found. Run this script from project root."
    exit 1
fi

cd frontend
echo "✅ Changed to frontend directory"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
npm ci  # Use npm ci instead of npm install for production builds
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Run build
echo "🔨 Building for production..."
npm run build
if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully"
else
    echo "❌ Build failed"
    exit 1
fi
echo ""

# Check if dist directory was created
if [ ! -d "dist" ]; then
    echo "❌ Build artifact directory 'dist' not found"
    exit 1
fi

echo "📁 Build artifacts in 'dist' directory:"
du -sh dist
echo ""

# Optional: Run Netlify CLI if installed
if command -v netlify &> /dev/null; then
    echo "🚀 Deploying to Netlify..."
    netlify deploy --prod
    if [ $? -eq 0 ]; then
        echo "✅ Deployment to Netlify successful!"
    else
        echo "⚠️  Netlify deployment had issues. Check Netlify Dashboard."
    fi
else
    echo "ℹ️  Netlify CLI not found. To deploy:"
    echo "   1. npm install -g netlify-cli"
    echo "   2. netlify login"
    echo "   3. netlify deploy --prod"
fi

echo ""
echo "================================"
echo "✅ Preparation complete!"
echo "================================"
echo ""
echo "Deployment locations:"
echo "  • Production: https://yourdomain.com"
echo "  • Dashboard: https://app.netlify.com"
echo "  • Documentation: See NETLIFY_BUILD_SETTINGS.md"
echo ""
