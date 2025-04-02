# Список переменный для cmd callback

import os
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
from app.classes import Transform
from config import SETTINGS as S
from app.conn.tables import UserEvent
from app.models.google_model import EventAnswer
from loguru import logger

class Cmd:
    """Класс для описания переменных используемых при вызове команд в боте"""
    cmd1 = "cmd1"   # Описание команды


# Текста кнопок
class KeyWords:
    """Клас для описания переменных используемых для клавиатуры в телеграмме"""

    create_event = "Создать событие"
    show_events = "Показать события"

    delete_event = "Удалить"
    delete_event_confirm = "Подтвердить удаление"
    edit_event = "Изменить"
    invite_event = "Пригласить"

    back = "Назад"


class Keyboard:
    """Класс для создания клавиатур"""

    @staticmethod
    def event_menu(user_id: int) -> InlineKeyboardMarkup:  # Клавиатура управления ботом

        event_menu = InlineKeyboardBuilder()
        event_menu.button(text=KeyWords.create_event, web_app=WebAppInfo(url=os.path.join(S.CALABRA_FRONT, S.ENDPOINT_CREATE_EVENT, str(user_id))))
        event_menu.button(text=KeyWords.show_events, callback_data=Transform(cmd=Cmd.show_events).str)
        event_menu.adjust(1)
        return event_menu.as_markup()

    @staticmethod
    def event_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:  # Клавиатура управления ботом

        kb = [[
            KeyboardButton(text=KeyWords.create_event, web_app=WebAppInfo(url=os.path.join(S.CALABRA_FRONT, S.ENDPOINT_CREATE_EVENT, str(user_id)))),
            KeyboardButton(text=KeyWords.show_events)
        ]]
        return ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True,
        )

    @staticmethod
    def event_manage(uuid: str) -> InlineKeyboardMarkup:  # Клавиатура управления событием

        event_manage = InlineKeyboardBuilder()
        event_manage.button(text=KeyWords.delete_event, callback_data=Transform(cmd=Cmd.delete_event, value=uuid).str)
        event_manage.button(text=KeyWords.edit_event, web_app=WebAppInfo(

            url=os.path.join(S.CALABRA_FRONT, S.ENDPOINT_SHOW_EVENT, uuid)
        ))
        event_manage.button(text=KeyWords.invite_event, callback_data=Transform(cmd=Cmd.invite_url, value=uuid).str)
        event_manage.adjust(3)
        return event_manage.as_markup()

    @staticmethod
    def confirm_delete_event(event_id: str) -> InlineKeyboardMarkup:
        event_manage = InlineKeyboardBuilder()
        event_manage.button(text=KeyWords.delete_event_confirm, callback_data=Transform(cmd=Cmd.confirm_delete_event, value=event_id).str)
        event_manage.button(text=KeyWords.back, callback_data=Transform(cmd=Cmd.dismiss_delete_event, value=event_id).str)
        event_manage.adjust(1)
        return event_manage.as_markup()

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
                    buttons = [[InlineKeyboardButton(text=coll.text, callback_data=Transform(cmd=Cmd.empty, value=value).str)]]
                    button_text = coll.text
                    break
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

        await BOT.b.edit_message_reply_markup(
            chat_id=callback.message.chat.id, message_id=callback.message.message_id, reply_markup=keyboard)
        return button_text

class BotMessages:

    @staticmethod
    async def prepare_event_text(_model: Union[EventAnswer, UserEvent], is_new:Union[bool, None] = None) -> str:

        # Шапка сообщения
        if is_new is None:
            message = ""
        else:
            message = "🎉 Событие успешно создано!\n" if is_new else "🔔 Событие изменено\n"

        logger.debug(f"Модель:\n\n{_model}")
        # Проверка даты
        try:
            if isinstance(_model, EventAnswer):     # Если пришло непосредственно событие
                start_time = _model.start.dateTime
                end_time = _model.end.dateTime
                attendees = [i.email for i in _model.attendees]

            else:     # Если пришли данные из базы
                start_time = _model.start
                end_time = _model.end
                attendees = _model.attendees.split(",")

        except Exception as e:
            message += f"Даты не распознаны: {e}"
            return message

        # Тело сообщения
        message += (
            f"📌 <b>{_model.summary}</b>\n"
            f"📅 Начало: <b>{date_to_format_text(str(start_time), _model.timezone)}</b>\n"
            f"🕒 Окончание: <b>{date_to_format_text(str(end_time), _model.timezone)}</b>\n"
            f"📍 Место встречи: {_model.location}\n"
            f"📝 Описание:\n<i>{_model.description}</i>\n"
            f"👤 Организатор:\n<i>{_model.initiator}</i>"
        )

        # Добавляем приглашенных если есть
        if attendees:

            # Удаляем email initiator из attendees
            initiator = _model.initiator.lower()
            attendees = list(map(str.lower, attendees))
            attendees = "\n".join([i for i in attendees if i != initiator])  # Оставляем всех кроме инициатора

            message += f'\n👥 Приглашенные:\n{attendees}'

        message += (
            f'\n\n📎 <a href="https://calabra.online/show-event/{_model.uuid}">Ссылка на событие</a>'
        )

        return message

    welcome_text = (
        f"👋 Привет, {{}}! Я — Calabra, твой помощник по управлению событиями!\n"
        f"✨ Что я умею:\n"
        f"• приглашать людей на события, когда вы не знаете их email\n"
        f"Как❓: \n"
        f"• создаю событие в боте и отправляю приглашаемым ссылку, чтобы они сами себя добавили к событию\n"
        f"Что ещё я могу❓:\n"
        f"• вносить изменения в событие и удалять его\n"
        f"Нажми «Создать событие»👇\n"
    )

    empty_events = f"Нет предстоящих событий"
    confirm_delete = f"Подтвердите удаление события?"
    fail_event_delete = f"Не удалось удалить событие"
    success_event_delete = f"Событие успешно удалено"

    invite_event_url = (
        f"📎 Пригласите новых участников по ссылке:\n"
        f"https://calabra.online/show-event/{{}}"
    )


if __name__ == '__main__':
    pass
