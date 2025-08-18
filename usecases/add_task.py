from datetime import datetime

from domain.models import Task, TaskId

from .ports import AddTaskRequest, Presenter, TaskRepository


class AddTask:

    def __init__(self, repo: TaskRepository, presenter: Presenter):
        self.repo = repo
        self.presenter = presenter

    def execute(self, req: AddTaskRequest) -> dict:
        title = (req.title or "").strip()
        if not title:
            return self.presenter.fail("Title cannot be empty.")

        task = Task(
            id=TaskId.new(),
            title=title,
            done=False,
            created_at=req.created_at or datetime.utcnow(),
        )
        self.repo.add(task=task)
        return self.presenter.success({"id": task.id.value})
