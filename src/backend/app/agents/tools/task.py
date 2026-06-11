from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASK_STORE_ENV = "TODOODOT_TASK_STORE"
DEFAULT_TASK_STORE = Path(__file__).resolve().parents[1] / "data" / "tasks.json"


def _task_store_path() -> Path:
    configured_path = os.getenv(TASK_STORE_ENV)
    if configured_path:
        return Path(configured_path).expanduser().resolve()
    return DEFAULT_TASK_STORE


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read_tasks() -> list[dict[str, Any]]:
    task_store = _task_store_path()
    if not task_store.exists():
        return []
    if task_store.stat().st_size == 0:
        return []

    with task_store.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"Task store must contain a JSON list: {task_store}")

    return data


def _write_tasks(tasks: list[dict[str, Any]]) -> None:
    task_store = _task_store_path()
    task_store.parent.mkdir(parents=True, exist_ok=True)

    with task_store.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2, ensure_ascii=False)
        file.write("\n")


def list_task(include_completed: bool = True) -> list[dict[str, Any]]:
    """List local tasks.

    Args:
        include_completed: Include completed tasks when true.
    """
    tasks = _read_tasks()
    if include_completed:
        return tasks

    return [task for task in tasks if task.get("status") != "completed"]


def add_task(title: str, description: str = "") -> dict[str, Any]:
    """Add a local task and return the created task."""
    cleaned_title = title.strip()
    cleaned_description = description.strip()

    if not cleaned_title:
        raise ValueError("Task title is required.")

    tasks = _read_tasks()
    next_id = max((int(task.get("id", 0)) for task in tasks), default=0) + 1

    task = {
        "id": next_id,
        "title": cleaned_title,
        "description": cleaned_description,
        "status": "pending",
        "created_at": _now(),
        "completed_at": None,
    }

    tasks.append(task)
    _write_tasks(tasks)
    return task


def complete_task(task_id: int) -> dict[str, Any]:
    """Mark a local task as completed by id and return the updated task."""
    tasks = _read_tasks()

    for task in tasks:
        if int(task.get("id", 0)) == task_id:
            task["status"] = "completed"
            task["completed_at"] = _now()
            _write_tasks(tasks)
            return task

    raise ValueError(f"Task not found: {task_id}")
