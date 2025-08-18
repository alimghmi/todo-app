from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Optional, Protocol

from domain.models import Task, TaskId


class TaskRepository(Protocol):
    def add(self, task: Task) -> None: ...
    def get(self, id: TaskId) -> Optional[Task]: ...
    def list(self) -> Iterable[Task]: ...
    def save(self, task: Task) -> None: ...


class Presenter(Protocol):
    def success(self, data) -> dict: ...
    def fail(self, message: str, *, status: int = 400) -> dict: ...


@dataclass
class AddTaskRequest:
    title: str
    created_at: datetime | None = None
