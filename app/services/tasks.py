from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tasks import TaskRepository
import app.schemas as schemas

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repo = TaskRepository(db)

    async def get_user_tasks(self, user_id: int):
        return await self.repo.get_tasks(user_id)

    async def create_new_task(self, task_data: schemas.TaskCreate, user_id: int):
        return await self.repo.create_task(task_data, user_id)

    async def get_task_by_id(self, task_id: int, user_id: int):
        return await self.repo.get_task(task_id, user_id)

    async def remove_task(self, task_id: int, user_id: int):
        return await self.repo.delete_task(task_id, user_id)