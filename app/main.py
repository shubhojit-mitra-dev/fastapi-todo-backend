from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger
# from app.db.database import connect_to_db, close_db_connection, fetch_version
from app.db.init_db import init_db, close_db_connection, fetch_version


app = FastAPI(title=settings.app_name)

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up the application")
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application")
    await close_db_connection()

@app.get("/health")
def health_check():
    logger.info("Health check performed")
    return {
        "status": "ok",
        "environment": settings.environment
    }

@app.get("/db-check")
async def db_check():
    version = await fetch_version()
    logger.info("Database version fetched")
    return {
        "status": "ok",
        "database_version": version
    }