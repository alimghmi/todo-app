from abc import ABC, abstractmethod
from typing import Iterable

from entities.models import Task, TaskId


class TaskServiceInterface(ABC):
    """Use case boundary for task operations."""

    @abstractmethod
    def create_task(self, title: str) -> Task: ...

    @abstractmethod
    def list_tasks(self) -> Iterable[Task]: ...

    @abstractmethod
    def mark_done(self, task_id: TaskId) -> Task: ...

    @abstractmethod
    def reopen(self, task_id: TaskId) -> Task: ...

    @abstractmethod
    def rename(self, task_id: TaskId, new_title: str) -> Task: ...
