from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from entities.models import Task, TaskId
from interfaces.repository_interface import TaskRepository
from repositories.sqlite_repo import SQLiteTaskRepo
from usecases.task_services import TaskNotFoundError, TaskService, ValidationError


def get_repo() -> TaskRepository:
    return SQLiteTaskRepo("todo.db")


def get_service(repo: TaskRepository = Depends(get_repo)) -> TaskService:
    return TaskService(repo)


app = FastAPI(title="TODO (Clean Architecture)", version="1.0.0")


@app.on_event("shutdown")
def _shutdown():
    try:
        repo = get_repo()
        repo.close()
    except Exception:
        pass


class TaskOut(BaseModel):
    id: str
    title: str
    done: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, t: Task) -> "TaskOut":
        return cls(id=t.id.value, title=t.title, done=t.done, created_at=t.created_at)


class TaskCreateIn(BaseModel):
    title: str = Field(..., min_length=1)


class TaskRenameIn(BaseModel):
    title: str = Field(..., min_length=1)


def handle_usecase_errors(exc: Exception):
    if isinstance(exc, TaskNotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    if isinstance(exc, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)
        )
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal error"
    )


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok"}


@app.get("/tasks", response_model=List[TaskOut], tags=["tasks"])
def list_tasks(svc: TaskService = Depends(get_service)):
    try:
        items = svc.list_tasks()
        return [TaskOut.from_entity(t) for t in items]
    except Exception as e:
        handle_usecase_errors(e)


@app.post(
    "/tasks",
    response_model=TaskOut,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreateIn, svc: TaskService = Depends(get_service)):
    try:
        t = svc.create_task(payload.title)
        return TaskOut.from_entity(t)
    except Exception as e:
        handle_usecase_errors(e)


@app.get("/tasks/{task_id}", response_model=TaskOut, tags=["tasks"])
def get_task(task_id: str, svc: TaskService = Depends(get_service)):
    try:
        t = svc._require(TaskId(task_id))  # internal helper raises TaskNotFoundError
        return TaskOut.from_entity(t)
    except Exception as e:
        handle_usecase_errors(e)


@app.post("/tasks/{task_id}/done", response_model=TaskOut, tags=["tasks"])
def mark_done(task_id: str, svc: TaskService = Depends(get_service)):
    try:
        t = svc.mark_done(TaskId(task_id))
        return TaskOut.from_entity(t)
    except Exception as e:
        handle_usecase_errors(e)


@app.post("/tasks/{task_id}/reopen", response_model=TaskOut, tags=["tasks"])
def reopen(task_id: str, svc: TaskService = Depends(get_service)):
    try:
        t = svc.reopen(TaskId(task_id))
        return TaskOut.from_entity(t)
    except Exception as e:
        handle_usecase_errors(e)


@app.post("/tasks/{task_id}/rename", response_model=TaskOut, tags=["tasks"])
def rename(
    task_id: str, payload: TaskRenameIn, svc: TaskService = Depends(get_service)
):
    try:
        t = svc.rename(TaskId(task_id), payload.title)
        return TaskOut.from_entity(t)
    except Exception as e:
        handle_usecase_errors(e)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(
    task_id: str,
    repo: TaskRepository = Depends(get_repo),
    svc: TaskService = Depends(get_service),
):
    try:
        # delete is a persistence concern; we expose it directly via repo
        repo.delete(TaskId(task_id))
        return
    except Exception as e:
        handle_usecase_errors(e)
