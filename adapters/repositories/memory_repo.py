from typing import Dict, Iterable, Optional

from domain.models import Task, TaskId


class InMemoryTaskRepo:

    def __init__(self):
        self._db: Dict[str, Task] = {}

    def add(self, task: Task) -> None:
        self._db[task.id.value] = task

    def get(self, id: TaskId) -> Optional[Task]:
        return self._db.get(id.value)

    def list(self) -> Iterable[Task]:
        return list(self._db.values())

    def save(self, task: Task) -> None:
        self._db[task.id.value] = task
