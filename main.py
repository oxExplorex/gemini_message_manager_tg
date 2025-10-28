import asyncio

from aiogram import Dispatcher
from pyrogram import compose, filters
from pyrogram.handlers import MessageHandler

from _logging import bot_logger
from aiotask.telegram_parse_dialogs import starting_tg_parse_dialogs_handler

from db.main import connect_database, close_database
from filters.all_filters_app import file_spoiler_filter
from handlers import router
from handlers_app.user.file_spoiler import file_spoiler_handler
from handlers_app.user.gemini_handler import gemini_app_handler
from handlers_app.user.reply_post_handler import reply_post_handler
from loader import bot, loop, apps_session
from middlewares.media_group import AlbumMiddleware
from middlewares.update_user import UpdateUserMiddleware
from utils.others import send_log_to_active_bot


async def start_polling_bot():

    await connect_database()

    router.message.middleware(AlbumMiddleware())
    router.business_message.middleware(AlbumMiddleware())

    router.message.middleware(UpdateUserMiddleware())
    router.business_message.middleware(UpdateUserMiddleware())

    dp = Dispatcher()

    dp.include_router(router)

    for app in apps_session:
        app.add_handler(MessageHandler(
            gemini_app_handler,
            filters.command("", prefixes=".")
        ))

        app.add_handler(MessageHandler(
            reply_post_handler,
            filters.command("", prefixes="+")  # Или используй filters.regex
        ))

        app.add_handler(MessageHandler(
            file_spoiler_handler,
            (filters.photo | filters.video | filters.video_note) & file_spoiler_filter ))

    _ = loop.create_task(compose(apps_session))


    await asyncio.sleep(5)  # костыль


    _ = asyncio.create_task(starting_tg_parse_dialogs_handler())

    await send_log_to_active_bot(bot)
    bot_logger.info("Bot was started")

    await dp.start_polling(bot)

    await close_database()


if __name__ == "__main__":
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    loop.run_until_complete(start_polling_bot())


