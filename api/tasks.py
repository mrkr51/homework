from typing import List
from fastapi import APIRouter, HTTPException, status

from schemas.tasks import Task, TaskCreate, TaskUpdate
from services.tasks import task_service

tasks_router = APIRouter(prefix="/tasks", tags=["tasks"])

@tasks_router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskCreate) -> Task:
    return task_service.create_task(task_in)

@tasks_router.get("/", response_model=List[Task])
async def list_tasks() -> List[Task]:
    return task_service.list_tasks()

@tasks_router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int) -> Task:
    task = task_service.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@tasks_router.put("/{task_id}", response_model=Task)
async def update_task(task_id: int, task_in: TaskUpdate) -> Task:
    task = task_service.update_task(task_id, task_in)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@tasks_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int) -> None:
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return None
