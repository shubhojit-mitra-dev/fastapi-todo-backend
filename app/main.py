from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(title=settings.app_name)

@app.get("/health")
def health_check():
    logger.info("Health check performed")
    return {
        "status": "ok",
        "environment": settings.environment
        }