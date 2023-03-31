import enum
from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Kind(enum.Enum):
    Chain = enum.auto()
    Molecule = enum.auto()
    Reaction = enum.auto()


class TaskBase(SQLModel):
    name: str = Field(nullable=False)
    kind: Kind = Field(nullable=False)
    problem: str = Field(nullable=False)
    initial: Optional[str] = Field(default="")
    solution: str = Field(nullable=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    identifier: Optional[UUID] = Field(
        default_factory=uuid4, primary_key=True, unique=True,
        nullable=False, index=True
    )


class TaskCreate(TaskBase):
    pass


class TaskRead(TaskBase):
    identifier: UUID
