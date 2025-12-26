from app.db.engine import engine
from app.db.base import Base
from app.models.user import User
from app.models.todo import Todo


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def fetch_version():
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT version();"))
        version = result.scalar()
        return version

async def close_db_connection():
    await engine.dispose()