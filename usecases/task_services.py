# usecases/task_services.py
from datetime import datetime
from typing import Iterable

from entities.models import Task, TaskId
from interfaces.repository_interface import TaskRepository
from interfaces.task_interface import TaskServiceInterface


class TaskNotFoundError(Exception):
    pass


class ValidationError(Exception):
    pass


class TaskService(TaskServiceInterface):

    def __init__(self, repo: TaskRepository):
        self._repo = repo

    def create_task(self, title: str) -> Task:
        title = (title or "").strip()
        if not title:
            raise ValidationError("title cannot be empty")
        task = Task(
            id=TaskId.new(),
            title=title,
            done=False,
            created_at=datetime.utcnow(),
        )
        self._repo.add(task)
        return task

    def list_tasks(self) -> Iterable[Task]:
        return self._repo.list()

    def _require(self, task_id: TaskId) -> Task:
        task = self._repo.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id.value} not found")
        return task

    def mark_done(self, task_id: TaskId) -> Task:
        task = self._require(task_id)
        if task.done:
            return task
        # mutate then persist (your Task dataclass is mutable)
        task.done = True
        self._repo.save(task)
        return task

    def reopen(self, task_id: TaskId) -> Task:
        task = self._require(task_id)
        if not task.done:
            return task
        task.done = False
        self._repo.save(task)
        return task

    def rename(self, task_id: TaskId, new_title: str) -> Task:
        new_title = (new_title or "").strip()
        if not new_title:
            raise ValidationError("new title cannot be empty")
        task = self._require(task_id)
        if task.title == new_title:
            return task
        task.title = new_title
        self._repo.save(task)
        return task
