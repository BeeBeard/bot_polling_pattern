from fastapi import APIRouter
from fastapi import Request
from loguru import logger

r_healthcheck = APIRouter(tags=['HEALTHCHECK'])


@r_healthcheck.get(f"/healthcheck")
async def check_get(request: Request):
    """Для проверки get"""
    logger.info(request)
    return {"message": "ok"}


@r_healthcheck.post(f"/healthcheck")
async def check_post(request: Request):
    """Для проверки post"""
    logger.info(request)
    return {"message": "ok"}


# @r_healthcheck.get("/sentry-debug")
# async def trigger_error():
#     """Для проверки sentry"""
#
#     division_by_zero = 1 / 0
#
#     return {"message": False}
