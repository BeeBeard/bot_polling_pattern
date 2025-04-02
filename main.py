import pprint

import uvicorn
from config import CONFIG
from loguru import logger
import sys

class LogSetting:

    INFO = (
        "<green>{time:HH:mm:ss}</green> -> "
        "<b>{message}</b>\n")

    EXCEPTION = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | <yellow>[Line {line: >4} | {function: >4} | {file: >4}]:</yellow>\n"
        "<b>{message}</b>\n"
        f"===============\n"
        "{exception}\n"
        f"===============\n")

    ELSE = (
        "<green>{time:HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | <yellow>[Line {line: >4} | {function: >4} | {file: >4}]:</yellow>\n"
        "<b>{message}</b>\n")

    @staticmethod
    def get_format(record):
        if record["level"].name == "INFO":
            return LogSetting.INFO
        elif record["exception"]:
            return LogSetting.EXCEPTION
        else:
            return LogSetting.ELSE


# logger.remove(handler_id=None)
logger.configure(handlers=[{"sink": sys.stderr, "format": LogSetting.get_format}])

logger.add("logs/.log", rotation="06:00", compression="zip")
logger.add("logs/info/info.log", format=LogSetting.INFO, level="INFO", rotation="06:00", compression="zip")
logger.add("logs/debug/debug.log", format=LogSetting.ELSE, level="DEBUG", rotation="06:00", compression="zip")
logger.add("logs/error/error.log", format=LogSetting.ELSE, level="ERROR", rotation="06:00", compression="zip",
           backtrace=True, diagnose=True, catch=True)

@logger.catch
def main():

    # sentry_loguru = LoguruIntegration(
    #     level=LoggingLevels.INFO.value,  # Capture info and above as breadcrumbs
    #     event_level=LoggingLevels.ERROR.value  # Send errors as events
    # )
    #
    # sentry_sdk.init(
    #
    #     dsn=S.DSN,
    #     send_default_pii=True,
    #     integrations=[
    #         sentry_loguru,
    #     ],
    # )

    # Base.metadata.create_all(conn.engine)

    pprint.pprint(CONFIG.model_dump())
    try:

        logger.info(f"Запуск API-server")
        logger.info(f"IP: {CONFIG.api.ip}")
        logger.info(f"PORT: {CONFIG.api.port}")
        uvicorn.run(
            app="start_app:APP",
            # app=APP,
            host=CONFIG.api.ip,
            port=CONFIG.api.port,
            # root_path=CONFIG.project.root,
            log_level="debug",
            reload=True
        )

    except KeyboardInterrupt:
        logger.info(f"Сервер остановлен")
    except Exception as e:
        logger.exception(e)
    finally:
        logger.info(f"Выключение приложения")


if __name__ == "__main__":
    main()
