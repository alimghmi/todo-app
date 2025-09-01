# presentations/cli.py
import argparse

from entities.models import TaskId
from repositories.memory_repo import InMemoryTaskRepo
from usecases.task_services import TaskNotFoundError, TaskService, ValidationError


def main():
    parser = argparse.ArgumentParser(prog="todo", description="Clean Architecture TODO")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a new task")
    p_add.add_argument("title", help="task title")

    sub.add_parser("list", help="list tasks")

    p_done = sub.add_parser("done", help="mark task done")
    p_done.add_argument("id")

    p_reopen = sub.add_parser("reopen", help="reopen a done task")
    p_reopen.add_argument("id")

    p_rename = sub.add_parser("rename", help="rename a task")
    p_rename.add_argument("id")
    p_rename.add_argument("title")

    args = parser.parse_args()

    repo = InMemoryTaskRepo()
    service = TaskService(repo)

    try:
        if args.cmd == "add":
            t = service.create_task(args.title)
            print(f"added {t.id.value} | {t.title} | done={t.done}")
        elif args.cmd == "list":
            for t in service.list_tasks():
                print(f"{t.id.value} | {'✔' if t.done else '·'} | {t.title}")
        elif args.cmd == "done":
            t = service.mark_done(TaskId(args.id))
            print(f"done {t.id.value} | {t.title}")
        elif args.cmd == "reopen":
            t = service.reopen(TaskId(args.id))
            print(f"reopened {t.id.value} | {t.title}")
        elif args.cmd == "rename":
            t = service.rename(TaskId(args.id), args.title)
            print(f"renamed {t.id.value} | {t.title}")
    except ValidationError as e:
        print(f"validation error: {e}")
    except TaskNotFoundError as e:
        print(f"not found: {e}")


if __name__ == "__main__":
    main()
