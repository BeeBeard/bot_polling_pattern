# Список переменный для cmd callback

# import os
from typing import Union

from aiogram.types import (
    CallbackQuery,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    ReplyKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot import BOT
from app.assistant import Transform
from aiogram.filters.state import State, StatesGroup
from config import CONFIG


class BotCmd:
    """Класс для описания переменных используемых при вызове команд в боте"""
    cmd1 = "cmd1"   # Описание команды

    cmd_test1 = "cmd_test1"
    cmd_test2 = "cmd_test2"
    empty = "empty"


# Текста кнопок
class BotKeyWords:
    """Клас для описания переменных используемых для клавиатуры в телеграмме"""

    key_word1 = "Кнопка 1"
    key_word2 = "Кнопка 2"


class BotStates(StatesGroup):
    """Клас для хранения списка используемых состояний"""

    state_test = State()

class BotKeyboards:
    """Класс для создания клавиатур"""

    @staticmethod
    def test_show_menu(value: Union[str, int]) -> InlineKeyboardMarkup:  # Клавиатура под сообщением ботом
        event_menu = InlineKeyboardBuilder()
        event_menu.button(text=BotKeyWords.key_word1, web_app=WebAppInfo(url=CONFIG.miniapp.path))
        event_menu.button(text=BotKeyWords.key_word2, callback_data=Transform(cmd=BotCmd.cmd_test1, value=value).str)
        event_menu.adjust(1)
        return event_menu.as_markup()

    @staticmethod
    def test_show_state() -> InlineKeyboardMarkup:  # Клавиатура под сообщением ботом
        event_menu = InlineKeyboardBuilder()
        event_menu.button(text=BotKeyWords.key_word2, callback_data=Transform(cmd=BotCmd.cmd_test2).str)
        event_menu.adjust(1)
        return event_menu.as_markup()

    @staticmethod
    def test_menu_keyboard() -> ReplyKeyboardMarkup:  # Клавиатура управления ботом

        kb = [[
            # KeyboardButton(text=KeyWords.key_word1, web_app=WebAppInfo(url=os.path.join(S.CALABRA_FRONT, S.ENDPOINT_CREATE_EVENT))),
            KeyboardButton(text=BotKeyWords.key_word2)
        ]]
        return ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )

    @staticmethod
    async def edit_as_answered(callback: CallbackQuery) -> str:
        # Редактируем предыдущее сообщение так что остается только нажатая кнопка (callback = empty)
        await callback.answer()

        buttons = []
        button_text = ""

        tform = Transform(callback.data)
        if isinstance(tform.value, int):
            value = tform.value + 1
        else:
            value = 1

        for row in callback.message.reply_markup.inline_keyboard:
            for coll in row:
                if coll.callback_data == callback.data:
                    buttons = [[InlineKeyboardButton(text=coll.text, callback_data=Transform(cmd=BotCmd.empty, value=value).str)]]
                    button_text = coll.text
                    break
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await BOT.b.edit_message_reply_markup(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=keyboard)
        return button_text

class BotMessages:

    start = f"Тестовое стартовое сообщений"


if __name__ == '__main__':
    pass
