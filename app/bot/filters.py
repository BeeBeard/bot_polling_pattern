# Модуль с пользовательскими фильтрами

from aiogram.filters import Filter
from aiogram.types import CallbackQuery

from app.assistant import Transform


class IsCallCmd(Filter):

    def __init__(self, cmd: str = None) -> None:
        self.cmd = cmd

    async def __call__(self, msg: CallbackQuery) -> bool:
        cmd = Transform(msg.data).cmd
        if self.cmd == cmd:
            return True
        return False


if __name__ == '__main__':
    pass
