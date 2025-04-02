from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

r_any = Router(name="r_group_any")


# отработка команд
async def cmd_start(message: Message) -> None:

    logger.info(message.text)
    await message.answer(message.text)


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))


if __name__ == '__main__':
    pass
