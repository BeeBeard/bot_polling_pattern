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
    await message.answer(f"{user}, отработала конечная функция echo для r_final_any роутера ({message.chat.type})")


async def cmd_start(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, Вы вызвали команду /start в r_final_any роутере ({message.chat.type})")


r_any.message.register(echo)

# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))

if __name__ == '__main__':
    pass
