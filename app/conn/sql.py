# Модуль с запросами к базе данных

from datetime import datetime
from typing import Union
from loguru import logger
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept as Dai

from app.conn import CONN
from app.conn import tables


async_engine = CONN.async_engine


# Добавляем данные к выбранной таблице
async def to_table(table: Dai = None, **kwargs) -> Union[tables.User, bool]:
    if not table or not kwargs:
        return False

    async with async_engine.connect() as session:

        try:
            kwargs["updated"] = datetime.now()
            clear_kwargs = {i: kwargs[i] for i in kwargs if i in table.__table__.columns.keys()}  # type: ignore
            # pprint.pprint(clear_kwargs)
            stmt = insert(table).values(**clear_kwargs)
            # print(stmt.compile(compile_kwargs={"literal_binds": True}))
            stmt = stmt.on_duplicate_key_update(**clear_kwargs)  # вставляем и возвращаем строку
            await session.execute(stmt)
            await session.commit()
            return True

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)
            return False


async def get_user(user_id: int) -> Union[tables.User, bool]:
    if not user_id:
        return False

    async with async_engine.connect() as session:

        try:
            stmt = (select(tables.User).filter(tables.User.user_id == user_id))
            result = await session.execute(stmt)

            return result.all()

        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(e)
            return False


if __name__ == '__main__':
    pass
