import asyncpg
from app.core.config import settings
from app.core.logging import logger

_pool: asyncpg.Pool | None = None


async def connect_to_db():
    global _pool

    logger.info("Creating PostgreSQL connection pool")

    _pool = await asyncpg.create_pool(
        dsn=settings.database_url,
        min_size=1,
        max_size=10,
    )


async def close_db_connection():
    global _pool

    if _pool:
        logger.info("Closing PostgreSQL connection pool")
        await _pool.close()


async def fetch_version():
    async with _pool.acquire() as conn:
        return await conn.fetchval("SELECT version();")
