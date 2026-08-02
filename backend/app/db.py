from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import Settings

settings = Settings()
engine = create_async_engine(settings.postgres_async_dsn, echo=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with AsyncSession(engine) as session:
        yield session
