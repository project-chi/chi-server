import os
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

dialect = "postgresql+asyncpg"
credentials = os.environ.get("DB_CREDENTIALS")
address = os.environ.get("DB_ADDRESS")
name = os.environ.get("DB_NAME")

url = f"{dialect}://{credentials}@{address}/{name}"
engine = create_async_engine(url)
session_creator = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with session_creator() as session:
        yield session


SessionDepends = Annotated[AsyncSession, Depends(get_async_session)]
