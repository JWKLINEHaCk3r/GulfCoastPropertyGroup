"""
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import logging.config

from .config import settings
from .database import init_db, close_db
from .agents import init_agents
from .api import leads, offers, buyers, deals, seo, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI-Powered Real Estate Wholesale Ecosystem",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(health.router, prefix="/api/v1/health", tags=["health"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["leads"])
app.include_router(offers.router, prefix="/api/v1/offers", tags=["offers"])
app.include_router(buyers.router, prefix="/api/v1/buyers", tags=["buyers"])
app.include_router(deals.router, prefix="/api/v1/deals", tags=["deals"])
app.include_router(seo.router, prefix="/api/v1/seo", tags=["seo"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    
    # Initialize database
    try:
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
    
    # Initialize agents
    try:
        init_agents()
        logger.info("✅ AI Agents initialized")
    except Exception as e:
        logger.error(f"❌ Agent initialization failed: {e}")
    
    logger.info("🎯 Application ready for business!")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("🛑 Shutting down application...")
    try:
        from .database import close_db
        await close_db()
        logger.info("✅ Database connections closed")
    except Exception as e:
        logger.error(f"❌ Database cleanup failed: {e}")
    logger.info("Goodbye!")


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs",
        "api": "/api/v1"
    }


# Exception handler
@app.exception_handler(Exception)
async def exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
