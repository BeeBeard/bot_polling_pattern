# Модуль парсинга, и записи базовых данных бота по его токену

import re
import json
import requests
from loguru import logger

from aiogram import Bot
from dataclasses import dataclass
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.bot import DefaultBotProperties
from typing import Union
from dotenv import load_dotenv
from app.config import CONFIG
from aiogram.types import BotCommand

load_dotenv()

@dataclass(frozen=False)
class BotData:  # Данные бота

    b = None
    id: Union[int, None] = None
    title: str = ""
    name: str = ""
    url: str = ""
    start_url: str = ""
    add_url: str = ""

    def __init__(self, token: str = None):

        self.token: str = token

        if self.check_token():
            self.set_bot()
            self.get_info()

    def check_token(self):
        if self.token and re.findall(r'^\d{10}:[\w\W]{35}', self.token):
            return True
        return False

    def set_bot(self):
        self.id: int = int(self.token.split(":")[0])  # НЕ менять привязан к БОТУ!
        self.b = Bot(
            token=self.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )

    def get_info(self):

        url = f"https://api.telegram.org/bot{self.token}/getMe"
        result = requests.get(url=url)
        content = json.loads(result.content.decode('utf8'))
        self.title = content["result"]["first_name"]
        self.name = content["result"]["username"]
        self.url = f"https://t.me/{self.name}"  # НЕ менять привязан к БОТУ!
        self.start_url = f"{self.url}?start="
        self.add_url = f"t.me/{self.name}?startgroup"

    def set_commands(self) -> None:
        """Отобразить список команд для пользователя"""
        commands = [
            BotCommand(command=f"/start", description="Запуск бота"),
            BotCommand(command=f"/id", description="Узнать собственный user.id"),

        ]
        self.b.set_my_commands(commands)


BOT = BotData(token=CONFIG.bot.token.get_secret_value())

logger.info(f"Bot id: {BOT.id}")
logger.info(f"Bot title: {BOT.title}")
logger.info(f"Bot name: {BOT.name}")
logger.info(f"Bot url: {BOT.url}")

if __name__ == "__main__":
    pass
