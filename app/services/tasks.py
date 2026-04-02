from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.tasks import TaskRepository
import app.schemas as schemas
from app.exceptions import TaskNotFound

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TaskRepository(db)

    async def get_user_tasks(self, user_id: int):
        return await self.repo.get_tasks(user_id)

    async def get_task_by_id(self, task_id: int, user_id: int):
        task = await self.repo.get_task(task_id, user_id)
        if not task:
            raise TaskNotFound()
        return task

    async def create_new_task(self, task_data: schemas.TaskCreate, user_id: int):
        return await self.repo.create_task(task_data, user_id)

    async def update_task(self, task_id: int, task_data: schemas.TaskUpdate, user_id: int):
        task = await self.repo.update_task(task_id, task_data, user_id)
        if not task:
            raise TaskNotFound()
        return task

    async def remove_task(self, task_id: int, user_id: int):
        success = await self.repo.delete_task(task_id, user_id)
        if not success:
            raise TaskNotFound()
        return {"message": "Task deleted successfully"}