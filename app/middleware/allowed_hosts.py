from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from config import CONFIG

# Кастомный middleware для проверки IP
class AllowedHosts:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Получаем запрос (только для HTTP/HTTPS)
        if scope["type"] == "http":
            request = Request(scope, receive)
            client_ip = request.client.host  # IP клиента

            # Если IP не разрешен — блокируем запрос
            if client_ip not in CONFIG.allowed.ips:
                response = JSONResponse(
                    status_code=403,
                    content={"error": "Forbidden", "message": "Доступ с вашего IP запрещен"},
                )
                await response(scope, receive, send)
                return

        # Если IP разрешен — продолжаем обработку
        await self.app(scope, receive, send)


if __name__ == "__main__":
    pass
