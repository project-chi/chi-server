from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from .task import Kind, Task, TaskBase, TaskCreate, TaskRead


async def initialize_database(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
