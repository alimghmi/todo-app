import argparse
import json

from adapters.presenters.json_presenter import JSONPresenter
from adapters.repositories.memory_repo import InMemoryTaskRepo
from usecases.add_task import AddTask
from usecases.list_tasks import ListTasks
from usecases.ports import AddTaskRequest
from usecases.toggle_task import ToggleTask

repo = InMemoryTaskRepo()
presenter = JSONPresenter()


def main():
    parser = argparse.ArgumentParser(prog="todo")
    subs = parser.add_subparsers(dest="cmd", required=True)

    p_add = subs.add_parser("add", help="Add a task")
    p_add.add_argument("title", type=str)

    subs.add_parser("list", help="List tasks")

    p_toggle = subs.add_parser("toggle", help="Toggle done/undone")
    p_toggle.add_argument("id", type=str)

    args = parser.parse_args()

    if args.cmd == "add":
        res = AddTask(repo, presenter).execute(AddTaskRequest(title=args.title))
    elif args.cmd == "list":
        res = ListTasks(repo, presenter).execute()
    else:
        res = ToggleTask(repo, presenter).execute(args.id)

    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
