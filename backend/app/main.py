"""
D'PARIS EGSOTIS – FastAPI Application Entry Point
Direktori Statistik Pariwisata Berbasis GPS & Infografis
"""
from contextlib import asynccontextmanager

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.router import api_router
from app.db.init_db import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    setup_logging()
    await init_db()
    yield


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="REST API untuk D'PARIS EGSOTIS – Direktori Statistik Pariwisata Kota Pagar Alam",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        openapi_url="/openapi.json" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate Limiting
    from app.middlewares.rate_limit import RateLimitMiddleware
    application.add_middleware(RateLimitMiddleware)

    # Static files (uploads)
    application.mount("/static", StaticFiles(directory="static"), name="static")

    # API routes (Using /api prefix for Vercel/Netlify consistency)
    application.include_router(api_router, prefix="/api")

    @application.get("/", tags=["Health"])
    async def health_check():
        # Prefer serving index.html if frontend is built
        if os.path.exists("dist/index.html"):
            return FileResponse("dist/index.html")
        return {
            "status": "ok",
            "app": settings.APP_NAME,
            "version": settings.APP_VERSION,
        }

    # Mount frontend static files (must be after /api routes)
    if os.path.exists("dist"):
        application.mount("/", StaticFiles(directory="dist", html=True), name="frontend")
    
    # Catch-all for SPA routing
    @application.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if os.path.exists("dist/index.html"):
            return FileResponse("dist/index.html")
        return {"error": "Not Found"}

    return application


app = create_application()
