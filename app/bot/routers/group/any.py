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
    await message.answer(f"{user}, Вы написали в группу, сработал роутер r_group_any  ({message.chat.type})")


async def cmd_start(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, Вы вызвали команду /start в группе, сработал роутер r_group_any ({message.chat.type})")

r_any.message.register(echo)

# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))


if __name__ == '__main__':
    pass
