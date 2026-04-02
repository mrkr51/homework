from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Comment
import app.schemas as schemas

class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_comment(self, comment_data: schemas.CommentCreate, task_id: int):
        db_comment = Comment(content=comment_data.content, task_id=task_id)
        self.db.add(db_comment)
        await self.db.commit()
        await self.db.refresh(db_comment)
        return db_comment

    async def get_comments_by_task(self, task_id: int):
        result = await self.db.execute(select(Comment).where(Comment.task_id == task_id))
        return result.scalars().all()