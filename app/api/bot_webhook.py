# Поднимаем Webhook для бота

from aiogram.types import Update
from fastapi import APIRouter, Request
from loguru import logger

from app.bot import BOT, DP
from config import CONFIG


r_bot_webhook = APIRouter(tags=['BOT WEBHOOK'])


# WEBHOOK
@r_bot_webhook.post(CONFIG.bot.root)
async def webhook(request: Request) -> None:
    logger.info("Получен запрос на bot webhook")

    # преобразовываем json в модель Update
    update = Update.model_validate(await request.json(), context={"bot": BOT.b})

    try:
        # Отправляем обрабатываться в подключенные роутеры
        await DP.feed_update(BOT.b, update)

    except Exception as e:
        logger.exception(e)

    logger.info("Запрос обработан")
# WEBHOOK


if __name__ == "__main__":
    pass
