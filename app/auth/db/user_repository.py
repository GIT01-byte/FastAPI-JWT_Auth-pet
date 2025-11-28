from sqlalchemy import select

from schemas.users import RegisterRequest
from models.users import UsersOrm

from db.database import Base, async_session_factory, async_engine


class UsersRepo():
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            async_engine.echo = False

    @staticmethod
    async def insert_user(payload: ...):
        async with async_session_factory() as session:
            user_dict = payload.model_dump()
            
            user = UsersOrm(**user_dict)
            session.add(user)
            await session.flush()
            await session.commit()

            return user.username
    
    @staticmethod
    async def select_user_by_username(username: str) -> UsersOrm | None:
        async with async_session_factory() as session:
            query = (
                select(UsersOrm)
                .where(UsersOrm.username == username)
            )
            result = await session.execute(query)
            user = result.scalars().first()
            return user
