# from loguru import logger
from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv

from app.assistant import Transform
from app.bot.content import BotKeyboards, Cmd
from app.bot.filters import IsCallCmd


load_dotenv()

r_any = Router(name="r_group_any")
r_any.message.filter(F.chat.type.in_({"group", "supergroup"}))


# Отработка команд

async def echo(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, Вы написали в группу, сработал роутер r_group_any  ({message.chat.type})")


async def cmd_start(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(
        text=f"{user}, Вы вызвали команду /start в группе, сработал роутер r_group_any ({message.chat.type})",
        reply_markup=BotKeyboards.test_menu()
    )


async def after_click_cmd_test(callback: CallbackQuery, tform: Transform) -> None:
    await callback.message.answer(text=f"Отработка нажатия кнопки в r_group_any cmd:{tform.cmd}")


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))

# Отработка нажатий кнопок в сообщениях
r_any.callback_query.register(after_click_cmd_test,              IsCallCmd(Cmd.cmd_test))

r_any.message.register(echo)


if __name__ == '__main__':
    pass
