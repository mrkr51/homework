from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
import app.schemas as schemas

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_tasks(self, owner_id: int):
        result = await self.session.execute(select(Task).where(Task.owner_id == owner_id))
        return result.scalars().all()

    async def create_task(self, task: schemas.TaskCreate, owner_id: int):
        db_task = Task(**task.model_dump(), owner_id=owner_id)
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)
        return db_task

    async def get_task_by_id(self, task_id: int, owner_id: int):
        result = await self.session.execute(
            select(Task).where(Task.id == task_id, Task.owner_id == owner_id)
        )
        return result.scalars().first()

    async def delete_task(self, task_id: int, owner_id: int):
        task = await self.get_task_by_id(task_id, owner_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        return False