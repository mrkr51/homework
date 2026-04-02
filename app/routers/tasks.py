from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.tasks import TaskService
from app.routers.auth import get_current_user
import app.schemas as schemas

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=list[schemas.Task])
async def read_tasks(current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.get_user_tasks(current_user.id)

@router.post("/", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    return await service.create_new_task(task, current_user.id)


@router.get("/{task_id}", response_model=schemas.Task)
async def read_task(task_id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    task = await service.get_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/{task_id}")
async def delete_task(task_id: int, current_user = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    service = TaskService(db)
    success = await service.remove_task(task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Deleted successfully"}