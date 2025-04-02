from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger
from aiogram import F

load_dotenv()

r_any = Router(name="r_final_any")


# Отработка команд

async def echo(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, отработала конечная функция echo для ({message.chat.type})")


# Отработка вводимых команд
r_any.message.register(echo)

if __name__ == '__main__':
    pass
