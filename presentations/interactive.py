from entities.models import TaskId
from repositories.sqlite_repo import SQLiteTaskRepo
from usecases.task_services import TaskNotFoundError, TaskService, ValidationError

HELP = """commands:
  add <title>
  list
  done <id>
  reopen <id>
  rename <id> <new_title>
  help
  quit
"""


def run():
    repo = SQLiteTaskRepo()
    svc = TaskService(repo)
    print("TODO REPL (clean architecture)\n" + HELP)
    while True:
        try:
            line = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nbye!")
            return
        if not line:
            continue
        if line in {"quit", "exit"}:
            print("bye!")
            return
        if line == "help":
            print(HELP)
            continue

        try:
            if line.startswith("add "):
                title = line[4:].strip()
                t = svc.create_task(title)
                print(f"added: {t.id.value} | {t.title}")

            elif line == "list":
                for t in svc.list_tasks():
                    print(f"{t.id.value} | {'✔' if t.done else '·'} | {t.title}")

            elif line.startswith("done "):
                _id = line.split(maxsplit=1)[1]
                t = svc.mark_done(TaskId(_id))
                print(f"done: {t.id.value} | {t.title}")

            elif line.startswith("reopen "):
                _id = line.split(maxsplit=1)[1]
                t = svc.reopen(TaskId(_id))
                print(f"reopened: {t.id.value} | {t.title}")

            elif line.startswith("rename "):
                parts = line.split(maxsplit=2)
                if len(parts) < 3:
                    print("usage: rename <id> <new_title>")
                else:
                    _id, new_title = parts[1], parts[2]
                    t = svc.rename(TaskId(_id), new_title)
                    print(f"renamed: {t.id.value} | {t.title}")

            else:
                print("unknown command. type 'help'")
        except ValidationError as e:
            print(f"validation error: {e}")
        except TaskNotFoundError as e:
            print(f"not found: {e}")


if __name__ == "__main__":
    run()
