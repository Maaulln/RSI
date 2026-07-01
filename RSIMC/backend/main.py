"""
DARSI-CS FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import settings
from app.database import init_db
from app.api import (
    auth, 
    nodes, 
    triage, 
    biometrics, 
    pharmacy, 
    integration, 
    admin
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown event handler
    """
    logger.info("🚀 Starting DARSI-CS Backend")
    await init_db()
    
    yield
    
    logger.info("🛑 Shutting down DARSI-CS Backend")


# Initialize FastAPI app
app = FastAPI(
    title="DARSI-CS API",
    description="Hospital AI Customer Service Backend",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,
    )


# Health Check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "darsi-cs-backend",
        "version": "1.0.0"
    }


# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(nodes.router, prefix="/api/nodes", tags=["Nodes"])
app.include_router(triage.router, prefix="/api/triage", tags=["Triage"])
app.include_router(biometrics.router, prefix="/api/biometrics", tags=["Biometrics"])
app.include_router(pharmacy.router, prefix="/api/pharmacy", tags=["Pharmacy"])
app.include_router(integration.router, prefix="/api/integration", tags=["Integration"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DARSI-CS Backend API",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
