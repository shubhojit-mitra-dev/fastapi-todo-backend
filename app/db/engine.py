from sqlalchemy.ext.asyncio import create_async_engine
from app.core.config import settings

engine = create_async_engine(
    settings.database_url.replace("postgresql://", "postgresql+psycopg://"),
    pool_size=10,
    max_overflow=5,
    pool_pre_ping=True,
)

async def dispose_engine():
    await engine.dispose()