from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

# from app.bot.middleware import Tform
# from app.bot.routers import r_cmd, r_private_all
from app.bot.routers import r_private, r_group


logger.info(f"Инициируем диспетчер")

DP = Dispatcher(storage=MemoryStorage())    # Инициируем диспетчер

# Подключаем middleware который будет выдавать Tform
# DP.callback_query.middleware.register(Tform())

# Список подключаемых роутеров
routers = [
    r_private.r_any,
    r_group.r_any
]

router_names = "\n".join([i.name for i in routers])
logger.info(f'Подключаем роутеры:\n{router_names}')


DP.include_routers(*routers)    # Подключаем роутеры

if __name__ == "__main__":
    pass
