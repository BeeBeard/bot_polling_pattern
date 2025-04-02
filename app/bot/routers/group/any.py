from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger
from aiogram import F

load_dotenv()

r_any = Router(name="r_group_any")
r_any.message.filter(F.chat.type.in_({"group", "supergroup"}))


# Отработка команд

async def echo(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, Вы написали в Группу ({message.chat.type})")

# Отработка вводимых команд
r_any.message.register(echo)


if __name__ == '__main__':
    pass
