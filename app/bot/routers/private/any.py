from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.assistant import Transform
from app.bot.content import BotKeyboards, BotStates, BotCmd
from app.bot.filters import IsCallCmd
from app.conn import tables, sql
from loguru import logger


r_any = Router(name="r_private_any")
r_any.message.filter(F.chat.type.in_({"private"}))


# Отработка команд
async def echo(msg: Message) -> None:
    """Тестовая функция для проверки работы бота"""

    user = msg.from_user.username or msg.from_user.first_name
    await msg.answer(f"{user}, Вы написали в ЛС ({msg.chat.type})")


async def cmd_start(msg: Message) -> None:
    """Тестовая функция для проверки вызова функции через команду /start"""

    try:
        user_data = msg.from_user.model_dump(exclude_none=True)
        user_data["user_id"] = msg.from_user.id

        await sql.to_table(table=tables.User, **user_data)

    except Exception as e:
        logger.error(f"Ошибка при сохранении данных пользователя: {e}")

    user = msg.from_user.username or msg.from_user.first_name
    await msg.answer(
        text=f"{user}, Вы вызвали команду /start в ЛС [{msg.chat.type}]",
        reply_markup=BotKeyboards.test_show_menu(value="Тестовое value private")
    )


async def after_click_cmd_test1(callback: CallbackQuery, state: FSMContext, tform: Transform) -> None:
    """Тестовая функция для проверки вызова функции нажатия на кнопку "Кнопка 1": callback - tform.cmd = cmd_test1"""

    await state.set_state(BotStates.state_test.state)   # Меняем состояние бота на state_test
    await state.update_data(value=tform.value)          # Добавляем атрибут для хранения и передачи в state

    await callback.answer()                             # Отключаем "мигание" кнопки после нажатия

    text = f"Отработка нажатия кнопки в ЛС cmd:{tform.cmd}. Введите текст для проверки state"
    await callback.message.answer(text=text)            # Отправляем сообщение пользователю


# noinspection PyUnusedLocal
async def after_click_cmd_test2(callback: CallbackQuery, state: FSMContext, tform: Transform) -> None:
    """Тестовая функция для проверки вызова функции нажатия на кнопку "Кнопка 2": callback - tform.cmd = cmd_test2"""

    state_data = await state.get_data()                 # Получаем данные из state
    await callback.answer()                             # Отключаем "мигание" кнопки после нажатия

    text = f"Ранее сохраненные данные:\n{state_data.get('value')}\n{state_data.get('text')}"
    await callback.message.answer(text=text)            # Отправляем сообщение пользователю

    await state.clear()                                 # Очищаем все состояния state


async def save_state_text(msg: Message, state: FSMContext):
    """Тестовая функция для сохранения msg.text в атрибут state"""

    await state.update_data(text=msg.text.strip())      # Добавляем атрибут для хранения и передачи в state
    await msg.answer(
        text="Ваше сообщение сохранено",
        reply_markup=BotKeyboards.test_show_state()
    )


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))

# Отработка нажатий кнопок в сообщениях
r_any.callback_query.register(after_click_cmd_test1, IsCallCmd(BotCmd.cmd_test1))
r_any.callback_query.register(after_click_cmd_test2, IsCallCmd(BotCmd.cmd_test2))

# Отработка state
r_any.message.register(save_state_text, StateFilter("BotStates:state_test"))

# Отработка обычных кнопок
r_any.message.register(echo)


if __name__ == '__main__':
    pass
