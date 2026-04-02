from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Task
import app.schemas as schemas

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_tasks(self, user_id: int):
        result = await self.db.execute(select(Task).where(Task.owner_id == user_id))
        return result.scalars().all()

    async def get_task(self, task_id: int, user_id: int):
        result = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.owner_id == user_id)
        )
        return result.scalars().first()

    async def create_task(self, task_data: schemas.TaskCreate, user_id: int):
        db_task = Task(**task_data.model_dump(), owner_id=user_id)
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def update_task(self, task_id: int, task_data: schemas.TaskUpdate, user_id: int):
        db_task = await self.get_task(task_id, user_id)
        if db_task:
            update_data = task_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_task, key, value)
            await self.db.commit()
            await self.db.refresh(db_task)
        return db_task

    async def delete_task(self, task_id: int, user_id: int):
        db_task = await self.get_task(task_id, user_id)
        if db_task:
            await self.db.delete(db_task)
            await self.db.commit()
            return True
        return False