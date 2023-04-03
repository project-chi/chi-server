import json
import logging.config
from typing import Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException
from sqlmodel import select

from chi_server.engine import SessionDepends, engine
from chi_server.models import (
    Task,
    TaskCreate,
    TaskRead,
    TaskUpdate,
    initialize_database,
)
from chi_server.paths import LOGGING_CONFIG

app = FastAPI(title="chi.server", version="0.2.0")
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


@app.post("/tasks", response_model=TaskRead)
async def create_task(session: SessionDepends, task: TaskCreate):
    database_task = Task.from_orm(task)

    session.add(database_task)
    await session.commit()
    await session.refresh(database_task)

    return database_task


@app.get("/tasks/{identifier}", response_model=Optional[TaskRead])
async def get_task(session: SessionDepends, identifier: UUID):
    statement = select(Task).where(Task.identifier == identifier)
    result = await session.execute(statement)
    task = result.scalar()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@app.patch("/tasks/{identifier}", response_model=TaskRead)
async def update_hero(session: SessionDepends, identifier: UUID, task: TaskUpdate):
    db_task = await session.get(Task, identifier)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@app.delete("/tasks/{identifier}", response_model=Optional[TaskRead])
async def delete_task(session: SessionDepends, identifier: UUID):
    statement = select(Task).where(Task.identifier == identifier)
    result = await session.execute(statement)
    task = result.scalar()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return task
