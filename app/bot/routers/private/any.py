# import pprint

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message  # CallbackQuery
from dotenv import load_dotenv
# from loguru import logger
from app.bot.content import BotKeyboards

load_dotenv()

r_any = Router(name="r_private_any")
r_any.message.filter(F.chat.type.in_({"private"}))


# Отработка команд
async def echo(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(f"{user}, Вы написали в ЛС ({message.chat.type})")


async def cmd_start(message: Message) -> None:
    user = message.from_user.username or message.from_user.first_name
    await message.answer(
        text=f"{user}, Вы вызвали команду /start в ЛС ({message.chat.type})",
        reply_markup=BotKeyboards.test_menu_keyboard()
    )


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))

r_any.message.register(echo)

# отработка нажатий кнопок в сообщениях
# r_private_all.callback_query.register(after_click_show_events,              IsCallCmd(Cmd.show_events))
# r_private_all.callback_query.register(after_click_delete_event,             IsCallCmd(Cmd.delete_event))
# r_private_all.callback_query.register(after_click_confirm_delete_event,     IsCallCmd(Cmd.confirm_delete_event))
# r_private_all.callback_query.register(after_click_dismiss_delete_event,     IsCallCmd(Cmd.dismiss_delete_event))
# r_private_all.callback_query.register(after_click_add_user,                 IsCallCmd(Cmd.invite_url))
# r_private_all.callback_query.register(after_click_empty,                    IsCallCmd(Cmd.empty))

# Отработка обычных кнопок
# r_private_all.message.register(kb_show_events, F.text == KeyWords.show_events)


if __name__ == '__main__':
    pass
