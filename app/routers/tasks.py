from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.tasks import TaskService
from app.routers.auth import get_current_user
from app.utils.s3 import s3_client
from app.config import MINIO_BUCKET
import app.schemas as schemas

router = APIRouter(prefix="/v1/tasks", tags=["tasks"])

@router.get("/", response_model=list[schemas.Task])
async def read_tasks(u=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await TaskService(db).get_user_tasks(u.id)

@router.post("/", response_model=schemas.Task)
async def create_task(t: schemas.TaskCreate, u=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await TaskService(db).create_new_task(t, u.id)

@router.post("/{task_id}/upload-avatar")
async def upload_task_avatar(task_id: int, file: UploadFile=File(...), u=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    await TaskService(db).get_task_by_id(task_id, u.id)
    content = await file.read()
    url = await s3_client.upload_file(content, f"task_{task_id}_{file.filename}", MINIO_BUCKET)
    return {"url": url}

@router.delete("/{task_id}")
async def delete_task(task_id: int, u=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    return await TaskService(db).remove_task(task_id, u.id)