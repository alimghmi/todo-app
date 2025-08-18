from domain.models import TaskId

from .ports import Presenter, TaskRepository


class ToggleTask:

    def __init__(self, repo: TaskRepository, presenter: Presenter):
        self.repo = repo
        self.presenter = presenter

    def execute(self, id: str) -> dict:
        task = self.repo.get(TaskId(id))
        if not task:
            return self.presenter.fail("Task not found.", status=404)

        task.done = not task.done
        self.repo.save(task)
        return self.presenter.success({"id": task.id.value, "done": task.done})
