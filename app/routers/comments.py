from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.comments import CommentService
from app.routers.auth import get_current_user
import app.schemas as schemas

router = APIRouter(prefix="/v1/tasks", tags=["comments"])

@router.post("/{task_id}/comments", response_model=schemas.Comment)
async def create_comment(
    task_id: int,
    comment: schemas.CommentCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = CommentService(db)
    return await service.add_comment(task_id, comment, current_user.id)

@router.get("/{task_id}/comments", response_model=list[schemas.Comment])
async def get_comments(
    task_id: int,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = CommentService(db)
    return await service.get_task_comments(task_id, current_user.id)