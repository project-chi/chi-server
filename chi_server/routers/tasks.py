from typing import Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException
from sqlalchemy.future import select

from chi_server.engine import SessionDepends
from chi_server.models import Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}}
)


@router.post("", response_model=TaskRead)
async def create_task(session: SessionDepends, task: TaskCreate):
    db_task = Task.from_orm(task)

    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.get("", response_model=list[UUID])
async def get_task_uuids(session: SessionDepends):
    statement = select(Task.identifier)
    result = await session.execute(statement)
    return result.scalars().all()


@router.get("/raw", response_model=list[TaskRead])
async def get_tasks(session: SessionDepends):
    statement = select(Task)
    result = await session.execute(statement)
    return result.scalars().all()


@router.get("/{identifier}", response_model=TaskRead)
async def get_task(session: SessionDepends, identifier: UUID):
    statement = select(Task).where(Task.identifier == identifier)
    result = await session.execute(statement)
    task = result.scalar()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.patch("/{identifier}", response_model=TaskRead)
async def update_task(session: SessionDepends, identifier: UUID, task: TaskUpdate):
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


@router.delete("/{identifier}", response_model=TaskRead)
async def delete_task(session: SessionDepends, identifier: UUID):
    statement = select(Task).where(Task.identifier == identifier)
    result = await session.execute(statement)
    task = result.scalar()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()

    return task
