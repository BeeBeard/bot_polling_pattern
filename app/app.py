# объявляем app FastAPI, поднимаем WebHook для бота

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api import r_healthcheck, r_bot_webhook

from app.bot import BOT, DP
from config import CONFIG


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(myapp: FastAPI):  # type: ignore
    # Код, выполняющийся при запуске приложения

    logger.info(f"Запуск Fast API")
    logger.info(f"Документация: {CONFIG.api.host}:{CONFIG.api.port}{CONFIG.project.root}/docs#")
    webhook = f"{CONFIG.bot.host}{CONFIG.project.root}{CONFIG.bot.webhook}"
    logger.info(f"Webhook: {webhook}")

    try:
        await BOT.b.set_webhook(
            url=webhook,
            allowed_updates=DP.resolve_used_update_types(),
            drop_pending_updates=True,
            secret_token=CONFIG.bot.secret.get_secret_value()
        )

        logger.info(f"Подключил веб-хук: {webhook}")
        yield  # Приложение работает

        # Код, выполняющийся при завершении работы приложения

        await BOT.b.delete_webhook()
        logger.info(f"Отключил веб-хук: {webhook}")
        logger.info(f"Остановка Fast API")
    except Exception as e:
        logger.error(e)
        yield


# Список сайтов с которыми доступно взаимодействие через API
origins = [
    # "http://calabra.online",
    # "https://calabra.online"
]

APP = FastAPI(root_path=CONFIG.project.root, lifespan=lifespan)
APP.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

APP.include_router(router=r_bot_webhook)    # Webhook для приема данных от API telegram
APP.include_router(router=r_healthcheck)    # router для проверки состояния приложения

if __name__ == "__main__":
    pass
