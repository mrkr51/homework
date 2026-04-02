from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.comments import CommentRepository
from app.repositories.tasks import TaskRepository
from app.exceptions import TaskNotFound
import app.schemas as schemas

class CommentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CommentRepository(db)
        self.task_repo = TaskRepository(db)

    async def add_comment(self, task_id: int, comment_data: schemas.CommentCreate, user_id: int):
        task = await self.task_repo.get_task(task_id, user_id)
        if not task:
            raise TaskNotFound()
        return await self.repo.create_comment(comment_data, task_id)

    async def get_task_comments(self, task_id: int, user_id: int):
        task = await self.task_repo.get_task(task_id, user_id)
        if not task:
            raise TaskNotFound()
        return await self.repo.get_comments_by_task(task_id)