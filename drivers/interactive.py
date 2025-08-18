import json

from adapters.presenters.human_presenter import HumanPresenter
from adapters.repositories.memory_repo import InMemoryTaskRepo
from usecases.add_task import AddTask
from usecases.list_tasks import ListTasks
from usecases.ports import AddTaskRequest
from usecases.toggle_task import ToggleTask

repo = InMemoryTaskRepo()
presenter = HumanPresenter()


def parse(input_text):
    tokens = input_text.strip().split(" ")
    cmd = tokens[0].lower()
    if cmd not in ["add", "list", "toggle"]:
        raise ValueError("Command not valid.")

    tokens.pop(0)
    arg = " ".join(tokens)
    return cmd, arg


def main():
    print(
        "\nTODO APP\n\nCommand lists:\n\t- add task_title\n\t- list\n\t- toggle task_id\n"
    )
    try:
        while True:
            cmd_raw = input("> ")
            try:
                cmd, arg = parse(cmd_raw)
                if cmd == "add":
                    res = AddTask(repo, presenter).execute(AddTaskRequest(title=arg))
                elif cmd == "list":
                    res = ListTasks(repo, presenter).execute()
                else:
                    res = ToggleTask(repo, presenter).execute(arg)

                print(res)
            except ValueError:
                print(">> Invalid command.")
                continue
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
