from __future__ import annotations
from typing import List, Optional
from schemas.tasks import Task, TaskCreate, TaskUpdate

class TaskService:
    def __init__(self) -> None:
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def list_tasks(self) -> List[Task]:
        return self._tasks

    def get_task(self, task_id: int) -> Optional[Task]:
        return next((task for task in self._tasks if task.id == task_id), None)

    def create_task(self, task_in: TaskCreate) -> Task:
        task = Task(id=self._next_id, **task_in.model_dump())
        self._next_id += 1
        self._tasks.append(task)
        return task

    def update_task(self, task_id: int, task_in: TaskUpdate) -> Optional[Task]:
        existing = self.get_task(task_id)
        if existing is None:
            return None

        update_data = task_in.model_dump(exclude_unset=True)
        updated = existing.model_copy(update=update_data)

        index = self._tasks.index(existing)
        self._tasks[index] = updated
        return updated

    def delete_task(self, task_id: int) -> bool:
        existing = self.get_task(task_id)
        if existing is None:
            return False
        self._tasks.remove(existing)
        return True

task_service = TaskService()
