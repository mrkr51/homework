from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
import app.schemas as schemas

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_username(self, username: str):
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def create_user(self, user: schemas.UserCreate, hashed_password: str):
        db_user = User(username=user.username, hashed_password=hashed_password)
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        return db_user