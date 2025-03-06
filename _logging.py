# - *- coding: utf- 8 - *-
import logging

import colorlog

from data.config import path_logs
from utils.datetime_tools import DateTime

bot_logger = logging.getLogger(__name__)

file_log = logging.FileHandler(path_logs.format(d=DateTime().time_strftime("%d.%m.%Y")), "a+", 'utf-8')
console_out = logging.StreamHandler()

format_message = colorlog.ColoredFormatter(
    "%(log_color)s[%(asctime)s | %(levelname)s]%(reset)s%(blue)s: %(filename)s | %(funcName)s:%(lineno)d - %(white)s%(message)s",
    datefmt="%d.%m.%Y %H:%M:%S",
    reset=True,
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'red,bg_white',
    }
)

console_out.setFormatter(format_message)

logging.basicConfig(handlers=(file_log, console_out),
                    format="[%(asctime)s | %(levelname)s]: %(filename)s | %(funcName)s:%(lineno)d - %(message)s",
                    datefmt='%m.%d.%Y %H:%M:%S',
                    level=logging.NOTSET)


def error_handler(type, value, tb):
    bot_logger.critical(f"Exception '{type.__name__}': {value}. File: '{tb.tb_frame.f_code.co_filename}'. Line: {tb.tb_lineno}")


logging.getLogger('aiogram').setLevel(logging.ERROR)
logging.getLogger('apscheduler').setLevel(logging.ERROR)
logging.getLogger('aiomysql').setLevel(logging.ERROR)
logging.getLogger('asyncio').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.ERROR)
logging.getLogger('pyrogram').setLevel(logging.INFO)
logging.getLogger('pyrotgfork').setLevel(logging.INFO)
logging.getLogger('aiohttp').setLevel(logging.INFO)
logging.getLogger('requests').setLevel(logging.INFO)
logging.getLogger('tortoise').setLevel(logging.INFO)



