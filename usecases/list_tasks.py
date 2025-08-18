from .ports import Presenter, TaskRepository


class ListTasks:

    def __init__(self, repo: TaskRepository, presenter: Presenter):
        self.repo = repo
        self.presenter = presenter

    def execute(self) -> dict:
        items = []
        for t in self.repo.list():
            items.append(
                {
                    "id": t.id.value,
                    "title": t.title,
                    "done": t.done,
                    "created_at": t.created_at.isoformat(),
                }
            )
        return self.presenter.success(items)
