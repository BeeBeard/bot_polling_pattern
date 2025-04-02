import pprint

from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from loguru import logger

# from app.bot.content import Cmd, Keyboard, KeyWords, BotMessages
# from app.bot.filters import IsCallCmd
# from app.classes import GoogleConnect, Transform
# from app.conn import sql

load_dotenv()

r_any = Router(name="r_private_any")



# отработка команд
async def cmd_start(message: Message) -> None:

    await message.answer(message.text)


# отработка кнопок сообщений
# async def after_click_show_events(callback: CallbackQuery) -> None:
#     await callback.answer()



# async def after_click_delete_event(callback: CallbackQuery, tform: Transform) -> None:
#     await callback.answer()
    # await callback.message.edit_reply_markup(reply_markup=Keyboard.confirm_delete_event(tform.value))


# async def after_click_confirm_delete_event(callback: CallbackQuery, tform: Transform) -> None:
#     await Keyboard.edit_as_answered(callback)
#
#     gc = GoogleConnect()
#
#     text = BotMessages.fail_event_delete
#     try:
#         data = await sql.get_event_by_uuid(tform.value)         # Получаем id события по uuid
#         result_api = gc.delete_event(event_id=data.id)          # удаляем событие из календаря
#         result_db = await sql.delete_event_by_uuid(uuid=tform.value)    # удаляем событие из базы
#
#         if result_api and result_db:
#             text = BotMessages.success_event_delete
#
#     except Exception as e:
#         logger.error(e)
#
#     await callback.answer(text=text)
#     await callback.message.delete()


# noinspection PyUnusedLocal
# async def after_click_dismiss_delete_event(callback: CallbackQuery, tform: Transform) -> None:
#     await callback.message.edit_reply_markup(reply_markup=Keyboard.event_manage(tform.value))


# async def after_click_add_user(callback: CallbackQuery, tform: Transform) -> None:
#     # await Keyboard.edit_as_answered(callback)
#     await callback.answer()
    # await callback.message.answer(text=BotMessages.invite_event_url.format(tform.value))


# noinspection PyUnusedLocal
# async def after_click_empty(callback: CallbackQuery, tform: Transform) -> None:
#     await Keyboard.edit_as_answered(callback)

# async def cmd_show_test(message: Message) -> None:
#     gc = GoogleConnect()  # создаем экземпляр для работы с гугл
#
#     colors = gc.get_colors()
#     pprint.pprint(colors.model_dump())
#
#     await message.answer(str(colors))


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))


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
