import os
import pprint

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import MiniappEvent
from config import CONFIG


templates_path = os.path.join("app", "templates")
templates = Jinja2Templates(directory=templates_path)

r_miniapp = APIRouter(prefix=CONFIG.miniapp.root, tags=['FRONTEND'])
r_invitation = APIRouter(tags=['INVITATION'])


@r_miniapp.get(f"/t1", response_class=HTMLResponse)
async def open_main_menu(request: Request):
    """
    Для проверки соединения
    Стартовая страница app
    """
    pprint.pprint(request)
    return templates.TemplateResponse(
        "pages/main_menu.html",
        {"request": request, 'active_tab': 'main_menu'}
    )


@r_miniapp.get(f"/t2", response_class=HTMLResponse)
async def open_create_event(request: Request, context: MiniappEvent = None):

    context = MiniappEvent.parse_obj(context) if context else MiniappEvent()
    context = context.model_dump()

    return templates.TemplateResponse(
        "pages/create_event.html",
        {"request": request, "context": context}
    )


# noinspection PyProtectedMember,PyUnresolvedReferences
@r_miniapp.get(f"/t3", response_class=HTMLResponse)
async def open_edit_event(event_id: str, request: Request, preload_context: MiniappEvent = None):

    if not preload_context:
        result = await sql.get_event(event_id=event_id)
        # noinspection PyUnresolvedReferences
        result_dict = result._asdict()
        pprint.pprint(f"Полученные данные из базы\n\n{result_dict}")
        context = MiniappEvent.parse_obj(result_dict)
        pprint.pprint(f"Схема \n\n{context}")

    else:
        context = MiniappEvent.parse_obj(preload_context)

    context.manage_type = "edit_event"

    return templates.TemplateResponse(
        "pages/create_event.html",
        {
            "request": request,
            "context": context
        }
    )


# Отдельный endpoint для короткой ссылки
# noinspection PyUnresolvedReferences,PyProtectedMember
@r_invitation.get("/{event_id}", response_class=HTMLResponse)
async def open_add_attendees(event_id: str, request: Request, preload_context: MiniappEvent = None):

    if not preload_context:
        result = await sql.get_event(event_id=event_id)
        # noinspection PyUnresolvedReferences,PyProtectedMember
        result_dict = result._asdict()
        pprint.pprint(f"Полученные данные из базы\n\n{result_dict}")
        context = MiniappEvent.parse_obj(result_dict)
        pprint.pprint(f"Схема \n\n{context}")

    else:
        context = MiniappEvent.parse_obj(preload_context)

    context.manage_type = "edit_event"

    return templates.TemplateResponse(
        "pages/add_attendees.html",
        {
            "request": request,
            "context": context
        }
    )


if __name__ == "__main__":
    pass
