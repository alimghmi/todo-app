import uuid
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class TaskId:
    value: str

    @staticmethod
    def new() -> "TaskId":
        return TaskId(str(uuid.uuid4()))


@dataclass
class Task:
    id: TaskId
    title: str
    done: bool
    created_at: datetime
