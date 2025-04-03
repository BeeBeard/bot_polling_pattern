from aiogram import F
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from app.assistant import Transform
from app.bot.content import BotKeyboards, BotStates, Cmd
from app.bot.filters import IsCallCmd

load_dotenv()

r_any = Router(name="r_private_any")
r_any.message.filter(F.chat.type.in_({"private"}))


# Отработка команд
async def echo(msg: Message) -> None:
    user = msg.from_user.username or msg.from_user.first_name
    await msg.answer(f"{user}, Вы написали в ЛС ({msg.chat.type})")


async def cmd_start(msg: Message) -> None:
    user = msg.from_user.username or msg.from_user.first_name
    await msg.answer(
        text=f"{user}, Вы вызвали команду /start в ЛС [{msg.chat.type}]",
        reply_markup=BotKeyboards.test_show_menu(value="Тестовое value")
    )


async def after_click_cmd_test1(callback: CallbackQuery, state: FSMContext, tform: Transform) -> None:

    # Меняем состояние бота
    await state.set_state(BotStates.state_test.state)
    await state.update_data(value=tform.value)

    await callback.answer()
    await callback.message.answer(
        text=(
            f"Отработка нажатия кнопки в ЛС cmd:{tform.cmd}. "
            f"Введите текст для проверки state"
        )
    )

async def after_click_cmd_test2(callback: CallbackQuery, state: FSMContext, tform: Transform) -> None:

    # Отображаем состояние бота
    state_data = await state.get_data()
    await callback.message.answer(
        text=(
            f"Ранее сохраненные данные:\n"
            f"{state_data.get('value')}\n"
            f"{state_data.get('text')}"
        )
    )


async def save_state_text(msg: Message, state: FSMContext):
    await state.update_data(text=msg.text.strip())
    await msg.answer(
        text="Ваше сообщение сохранено",
        reply_markup=BotKeyboards.test_show_state()
    )


# Отработка вводимых команд
r_any.message.register(cmd_start, Command("start"))

# Отработка нажатий кнопок в сообщениях
r_any.callback_query.register(after_click_cmd_test1, IsCallCmd(Cmd.cmd_test1))
r_any.callback_query.register(after_click_cmd_test2, IsCallCmd(Cmd.cmd_test2))

# Отработка state
r_any.message.register(save_state_text, StateFilter("BotStates:state_test"))

# Отработка обычных кнопок
r_any.message.register(echo)

# r_private_all.message.register(kb_show_events, F.text == KeyWords.show_events)


if __name__ == '__main__':
    pass
