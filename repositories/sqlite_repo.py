import sqlite3
from datetime import datetime
from typing import Iterable, List, Optional

from entities.models import Task, TaskId
from interfaces.repository_interface import TaskRepository

_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    done INTEGER NOT NULL CHECK (done IN (0,1)),
    created_at TEXT NOT NULL
);
"""


class SQLiteTaskRepo(TaskRepository):

    def __init__(self, db_path: str = "todo.db"):
        self._conn = sqlite3.connect(db_path)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA foreign_keys = ON;")
        self._conn.execute(_SCHEMA)
        self._conn.commit()

    @staticmethod
    def _to_iso(dt: datetime) -> str:
        return dt.isoformat(timespec="seconds")

    @staticmethod
    def _from_iso(s: str) -> datetime:
        return datetime.fromisoformat(s)

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> Task:
        return Task(
            id=TaskId(row["id"]),
            title=row["title"],
            done=bool(row["done"]),
            created_at=SQLiteTaskRepo._from_iso(row["created_at"]),
        )

    def add(self, task: Task) -> None:
        self._conn.execute(
            "INSERT INTO tasks (id, title, done, created_at) VALUES (?, ?, ?, ?)",
            (
                task.id.value,
                task.title,
                1 if task.done else 0,
                self._to_iso(task.created_at),
            ),
        )
        self._conn.commit()

    def get(self, id: TaskId) -> Optional[Task]:
        cur = self._conn.execute(
            "SELECT id, title, done, created_at FROM tasks WHERE id = ?", (id.value,)
        )
        row = cur.fetchone()
        return self._row_to_task(row) if row else None

    def list(self) -> Iterable[Task]:
        cur = self._conn.execute(
            "SELECT id, title, done, created_at FROM tasks ORDER BY created_at DESC"
        )
        rows: List[sqlite3.Row] = cur.fetchall()
        return [self._row_to_task(r) for r in rows]

    def save(self, task: Task) -> None:
        cur = self._conn.execute(
            "UPDATE tasks SET title = ?, done = ?, created_at = ? WHERE id = ?",
            (
                task.title,
                1 if task.done else 0,
                self._to_iso(task.created_at),
                task.id.value,
            ),
        )
        if cur.rowcount == 0:
            self.add(task)
        else:
            self._conn.commit()

    def delete(self, id: TaskId) -> None:
        self._conn.execute("DELETE FROM tasks WHERE id = ?", (id.value,))
        self._conn.commit()

    def close(self) -> None:
        try:
            self._conn.close()
        except Exception:
            pass
