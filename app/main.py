from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
from app.db.engine import dispose_engine
from sqlalchemy import text
from app.db.session import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title=settings.app_name)


@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    # nothing DB-specific required here


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    await dispose_engine()


@app.get("/health")
def health_check():
    logger.info("Health check performed")
    return {
        "status": "ok",
        "environment": settings.environment,
    }


@app.get("/db-check")
async def db_check(
    db: AsyncSession = Depends(get_db_session),
):
    result = await db.execute(text("SELECT version();"))
    version = result.scalar()
    return {
        "status": "ok",
        "database_version": version,
    }
