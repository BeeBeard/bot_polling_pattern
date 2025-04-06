import logging
from loguru import logger


# Перенаправляем стандартные логи в Loguru
class InterruptLogger(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


if __name__ == '__main__':
    pass
