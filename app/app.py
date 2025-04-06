# объявляем app FastAPI, поднимаем WebHook для бота

import os.path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.api import r_healthcheck, r_bot_webhook, r_miniapp
from app.bot import BOT, DP
from app.middleware import AllowedHosts
from app.config import CONFIG


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(myapp: FastAPI):  # type: ignore
    # Код, выполняющийся при запуске приложения

    logger.info(f"Запуск Fast API")
    logger.info(f"Документация: {CONFIG.api.host}:{CONFIG.api.port}{CONFIG.project.root}/docs#")
    logger.info(f"Корень miniapp: {CONFIG.miniapp.path}")
    logger.info(f"Webhook: {CONFIG.bot.webhook}")

    try:
        await BOT.b.set_webhook(
            url=CONFIG.bot.webhook,
            allowed_updates=DP.resolve_used_update_types(),
            drop_pending_updates=True,
            secret_token=CONFIG.bot.secret.get_secret_value()
        )

        logger.info(f"Подключил веб-хук: {CONFIG.bot.webhook}")
        yield  # Приложение работает

        # Код, выполняющийся при завершении работы приложения

        await BOT.b.delete_webhook()
        logger.info(f"Отключил веб-хук: {CONFIG.bot.webhook}")
        logger.info(f"Остановка Fast API")
    except Exception as e:
        logger.error(e)
        yield


# Список сайтов с которыми доступно взаимодействие через API
origins = []

APP = FastAPI(root_path=CONFIG.project.root, lifespan=lifespan)
APP.add_middleware(AllowedHosts)

# APP.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

APP.include_router(router=r_bot_webhook)    # Webhook для приема данных от API telegram
APP.include_router(router=r_healthcheck)    # router для проверки состояния приложения
APP.include_router(router=r_miniapp)


APP.mount(path='/static', app=StaticFiles(directory=os.path.join("app", "frontend", "static")), name='static')

if __name__ == "__main__":
    pass
