from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from sqlmodel import SQLModel

# from sqlalchemy import URL
# url = URL.create(
#     drivername="postgresql+asyncpg",
#     username="postgres",
#     password="root",
#     host="localhost",
#     port=5432,
#     database="TestDatabase"
# ).render_as_string(hide_password=False)
# print(url)

async_engine = AsyncEngine(
    create_engine(url=Config.DATABASE_URL, echo=False)
)

async def init_db():
    async with async_engine.begin() as conn:
        from models.Books import Book
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with session() as session:
        yield session