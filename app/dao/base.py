from app.database import async_session_maker
from sqlalchemy import insert, delete, select, update

class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none(cls, **filter):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_all(cls, **filter):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter)
            result = await session.execute(query)
            return result.scalars().all() 
    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**values).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def delete(cls, **filter):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**filter)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update(cls, filter_by: dict, values: dict):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
                .values(**values)
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()        