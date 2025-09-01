# interfaces/repository_interface.py
from abc import ABC, abstractmethod
from typing import Iterable, Optional

from entities.models import Task, TaskId


class TaskRepository(ABC):

    @abstractmethod
    def add(self, task: Task) -> None: ...

    @abstractmethod
    def get(self, id: TaskId) -> Optional[Task]: ...

    @abstractmethod
    def list(self) -> Iterable[Task]: ...

    @abstractmethod
    def save(self, task: Task) -> None: ...

    @abstractmethod
    def delete(self, id: TaskId) -> None: ...

    @abstractmethod
    def close(self) -> None: ...
