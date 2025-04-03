import os
import pprint

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import MiniappEvent
from config import CONFIG


templates_path = os.path.join("app", "frontend", "templates")  # Путь где фактически располагаются templates
templates = Jinja2Templates(directory=templates_path)

r_miniapp = APIRouter(prefix=CONFIG.miniapp.root, tags=['FRONTEND'])
r_invitation = APIRouter(tags=['INVITATION'])


@r_miniapp.get(f"/test_page", response_class=HTMLResponse)
async def open_main_menu(request: Request):
    """Для проверки соединения стартовая страница miniapp"""

    pprint.pprint(request)
    return templates.TemplateResponse(
        "pages/test_page.html",
        {"request": request, "root": CONFIG.project.root}
    )


if __name__ == "__main__":
    pass
