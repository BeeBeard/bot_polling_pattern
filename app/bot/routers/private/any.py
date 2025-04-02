import pprint

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from loguru import logger


load_dotenv()

r_any = Router(name="r_private_any")


# отработка команд
async def cmd_start(message: Message) -> None:
    logger.info(message)
    await message.answer(message.text)

# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))
# r_any.message.register(cmd_start)


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
