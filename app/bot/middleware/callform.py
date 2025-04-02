from loguru import logger

from typing import Any, Awaitable, Callable, Dict
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware

from app.assistant import Transform


class CallForm(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        """
        :param handler:
        :param event:
        :param data:
        :return:
        """

        tform = Transform(event.data)
        data["tform"] = tform

        logger.debug(f'Callback => chat_type: {data["event_chat"].type} | '
                     f'chat_id: {data["event_chat"].id} => {tform.dict}')

        result = await handler(event, data)
        return result


if __name__ == "__main__":
    pass
