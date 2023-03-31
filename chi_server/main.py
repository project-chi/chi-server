import json
import logging.config
from typing import Optional
from uuid import UUID

from fastapi import FastAPI
from sqlmodel import select

from chi_server.engine import SessionDepends, engine
from chi_server.models import Task, TaskCreate, TaskRead, initialize_database
from chi_server.paths import LOGGING_CONFIG

app = FastAPI()
logger = logging.getLogger("chi_server.main")
logging.config.dictConfig(json.loads(LOGGING_CONFIG.read_text()))


@app.on_event("startup")
async def on_startup():
    await initialize_database(engine)
    logger.info("Database initialized.")


@app.get("/tasks", response_model=list[UUID])
async def get_task_list(session: SessionDepends):
    statement = select(Task.identifier)
    result = await session.execute(statement)
    return result.scalars().all()


@app.post("/task", response_model=TaskRead)
async def create_task(session: SessionDepends, task: TaskCreate):
    database_task = Task.from_orm(task)

    session.add(database_task)
    await session.commit()
    await session.refresh(database_task)

    return database_task


@app.get("/task/{identifier}", response_model=Optional[TaskRead])
async def get_task(session: SessionDepends, identifier: UUID):
    statement = select(Task).where(Task.identifier == identifier)
    result = await session.execute(statement)
    return result.scalar()
