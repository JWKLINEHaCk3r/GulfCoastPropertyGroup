"""
Health check endpoints
"""
from fastapi import APIRouter, Depends
from datetime import datetime

from ..config import settings

router = APIRouter()


@router.get("/", tags=["health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.environment
    }


@router.get("/ready", tags=["health"])
async def readiness_check():
    """Readiness check endpoint"""
    return {
        "ready": True,
        "database": "connected",
        "agents": "initialized",
        "timestamp": datetime.utcnow().isoformat()
    }
