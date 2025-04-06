# Модуль инициализации таблиц и отношений для базы данных

from typing import Annotated

from sqlalchemy import BigInteger, Boolean, DateTime, text, String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.sql import func

from uuid import UUID

created = Annotated[str, mapped_column(DateTime(
    timezone=True), server_default=func.now(), nullable=False, index=True, comment='Время добавления')]

# При обновлении меняет дату обновления записи
updated = Annotated[str, mapped_column(DateTime(
    timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False, index=True, comment='Время обновления')]


# Декларативное создание
class Base(DeclarativeBase):
    type_annotation_map = {
        UUID: String(36)    # uuid.UUID → VARCHAR(36)
    }


# Таблица для хранения данных пользователей TG
class User(Base):  # Parent
    __tablename__ = "users"
    __table_args__ = {'comment': 'Данные пользователя из TG'}

    id = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False, index=True, autoincrement=True)
    user_id = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False, index=True, comment='ID пользователя')
    is_bot = mapped_column(Boolean, server_default=text('False'), nullable=False, comment='Это бот?')
    is_premium = mapped_column(Boolean, server_default=text('False'), nullable=True, comment='Есть премиум?')
    username = mapped_column(String(100), nullable=True, comment="Username")
    first_name = mapped_column(String(100), nullable=True, comment="Имя")
    last_name = mapped_column(String(100), nullable=True, comment="Фамилия")
    language_code = mapped_column(String(20), nullable=True, comment='Язык')

    def __repr__(self) -> str:
        return (
            f"User("
            f"id={self.id!r}, "
            f"user_id={self.user_id!r}, "
            f"is_bot={self.is_bot!r}, "
            f"is_premium={self.is_premium!r}, "
            f"username={self.username!r}, "
            f"first_name={self.first_name!r}, "
            f"last_name={self.last_name!r}, "
            f"language_code={self.language_code!r})"
        )


if __name__ == '__main__':
    pass
