# объявляем app FastAPI, поднимаем WebHook для бота

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.healthcheck import r_healthcheck

from app.bot import BOT, DP
from config import CONFIG


# noinspection PyUnusedLocal
@asynccontextmanager
async def lifespan(myapp: FastAPI):  # type: ignore
    # Код, выполняющийся при запуске приложения

    logger.info(f"Запуск Fast API")
    logger.info(f"Документация: {CONFIG.api.host}:{CONFIG.api.port}/docs#")
    logger.info(f"Webhook: https://{CONFIG.bot.path}")

    try:
        await BOT.b.set_webhook(
            url=CONFIG.bot.path,
            allowed_updates=DP.resolve_used_update_types(),
            drop_pending_updates=True,
            secret_token=CONFIG.bot.secret.get_secret_value()
        )

        logger.info(f"Подключил веб-хук: {CONFIG.bot.path}")
        yield  # Приложение работает

        # Код, выполняющийся при завершении работы приложения

        await BOT.b.delete_webhook()
        logger.info(f"Отключил веб-хук: {CONFIG.bot.path}")
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

# APP.include_router(router=r_webhook)
# APP.include_router(router=r_google_rest)
APP.include_router(router=r_healthcheck)

if __name__ == "__main__":
    pass
