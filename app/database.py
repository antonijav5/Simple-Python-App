from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///test.db"

engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with SessionLocal() as db:
        yield db
