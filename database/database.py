from sqlalchemy.ext.asyncio import  async_sessionmaker,create_async_engine,AsyncSession
from config import settings

engine = create_async_engine(settings.database_url())

SessionLocal = async_sessionmaker( bind=engine , autoflush=False )


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            db.close()





