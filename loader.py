import asyncio
import os
import traceback
import google.generativeai as genai
from aerich import Command
from aiogram import Bot, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from google.generativeai import ChatSession
from pyrogram import Client

from _logging import bot_logger
from config_statistic import SAFETY_SETTINGS
from data.config import GEMINI_KEY
from data.config import TOKEN_BOT
from db.main import connect_database, close_database, TORTOISE_ORM, delete_user, update_user, get_account_all, \
    get_app_tg_uuid_aio, get_admins

loop = asyncio.get_event_loop()
asyncio_lock = asyncio.Lock()


async def _check_and_migration_db():

    if not os.path.exists("./migrations"):
        os.makedirs("./migrations")
    if not os.path.exists("./migrations/models"):
        os.makedirs("./migrations/models")

    command = Command(tortoise_config=TORTOISE_ORM, app='models')

    try:
        await command.init_db(False)
    except:
        pass

    await command.init()
    try:
        await command.upgrade()
    except:
        pass
    await command.migrate()

    await connect_database()

    await delete_user(1)

    await update_user(1, "", "")

    await delete_user(1)

    await close_database()


async def _get_apps_user():
    try:
        await connect_database()

        _apps = [
        ]

        for _account in await get_account_all():

            _app_tg = await get_app_tg_uuid_aio(_account.app_tg)
            if not _app_tg:
                # todo alert admin
                continue

            _apps.append(
                Client(
                    name=f"data/session/{_account.number}",
                    api_id=_app_tg.app_id,
                    api_hash=_app_tg.api_hash,
                    phone_number=f"{_account.number}",
                )
            )


        await close_database()
        return _apps
    except Exception as e:

        bot_logger.info(traceback.format_exc())

        try:
            await close_database()
        except:
            pass
        return False


_ = loop.run_until_complete(_check_and_migration_db())  # миграция
_ = loop.run_until_complete(_check_and_migration_db())  # миграция
apps_session = loop.run_until_complete(_get_apps_user())


router = Router()
bot = Bot(
    token=TOKEN_BOT,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

async def _get_gemini_chat():
    try:
        await connect_database()

        if os.path.exists("data/proxy.txt"):
            with open("data/proxy.txt", "r") as file:
                _ip, _port, _user, _password = file.read().split(":")

            proxy = f'http://{_user}:{_password}@{_ip}:{_port}'

            bot_logger.info(f"Установлены прокси : {proxy}")

            os.environ['http_proxy'] = proxy
            os.environ['HTTP_PROXY'] = proxy
            os.environ['https_proxy'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
            os.environ['HTTPS_PROXY'] = proxy
            os.environ['grpc_proxy'] = proxy  # GRPC прокси
            os.environ['GRPC_PROXY'] = proxy  # GRPC прокси (верхний регистр)

        genai.configure(api_key=GEMINI_KEY)

        with open("data/promt_ai_userbot.txt", "r", encoding="utf-8") as file:
            SYSTEM_INSTRUCTION = file.read()

        _admins = list(set([x.user_id for x in await get_account_all()]))
        _admins = ", ".join([str(x) for x in _admins])

        bot_logger.info(_admins)

        model = genai.GenerativeModel(
            model_name='gemini-2.0-flash',
            system_instruction=SYSTEM_INSTRUCTION.replace("[Здесь перечислить user_id через запятую]", _admins),
            safety_settings=SAFETY_SETTINGS,

        )
        chat_gemini = model.start_chat(history=[])

        await close_database()
        return chat_gemini
    except Exception as e:

        bot_logger.info(traceback.format_exc())

        try:
            await close_database()
        except:
            pass
        return False

chat_gemini: ChatSession = loop.run_until_complete(_get_gemini_chat())
