import traceback
import asyncio
from typing import Callable, Any

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import html
from pyrogram.errors import RPCError, InternalServerError, FloodWait

from _logging import bot_logger
from db.main import (
    get_dump_chat_admin_all, update_user, get_user,
    create_dump_chat_user, del_dump_chat_user, get_account_tg_to_user_id
)
from loader import apps_session, bot
from utils.others import get_user_log_text

scheduler = AsyncIOScheduler()


async def safe_call(coro_func: Callable, *args: Any, retries: int = 3, delay: int = 2, **kwargs: Any) -> Any:
    for i in range(retries):
        try:
            return await coro_func(*args, **kwargs)
        except FloodWait as e:
            bot_logger.warning(f"FloodWait: sleeping for {e.value} seconds")
            await asyncio.sleep(e.value)
        except (RPCError, InternalServerError) as e:
            bot_logger.warning(f"Attempt {i + 1}/{retries} failed: {type(e).__name__} — {e}")
            await asyncio.sleep(delay * (2 ** i))
    bot_logger.error(f"All retries failed for {coro_func.__name__}")
    raise Exception(f"safe_call: all retries failed for {coro_func.__name__}")


def chunk_text(messages: list[str], max_length: int = 3500) -> list[str]:
    result, current = [], ""
    for msg in messages:
        if len(current) + len(msg) >= max_length:
            result.append(current)
            current = ""
        current += msg
    if current:
        result.append(current)
    return result


@scheduler.scheduled_job('interval', minutes=20)
async def __tg_parse_dialogs_handler():
    try:
        if not apps_session:
            return bot_logger.error("apps_session is None")

        for app_session in apps_session:
            try:
                admin_id = (await safe_call(app_session.get_me)).id

                existing_chat_ids = {x.chat_id for x in await get_dump_chat_admin_all(admin_id)}
                current_chat_ids = set()
                new_chats = []

                total_dialogs = (
                    await safe_call(app_session.get_dialogs_count, pinned_only=None, chat_list=0) +
                    await safe_call(app_session.get_dialogs_count, pinned_only=None, chat_list=1)
                )

                bot_logger.info(f'START USER: {admin_id} | {total_dialogs}')

                try:
                    async for dialog in app_session.get_dialogs(limit=total_dialogs + 10, pinned_only=True, chat_list=None):
                        chat_id = dialog.chat.id
                        username = dialog.chat.username
                        chat_name = dialog.chat.full_name or dialog.chat.title

                        if chat_id not in current_chat_ids:
                            current_chat_ids.add(chat_id)

                            await update_user(chat_id, username, chat_name)

                            if chat_id not in existing_chat_ids:
                                new_chats.append(chat_id)
                except (RPCError, InternalServerError) as e:
                    bot_logger.warning(f"get_dialogs error: {e}")
                    continue

                # Новые и удалённые чаты
                deleted_chats = existing_chat_ids - current_chat_ids
                all_changes = new_chats + list(deleted_chats)

                log_new = []
                log_del = []

                for chat_id in all_changes:
                    user = await get_user(chat_id)
                    username = user.username if user else "Ошибка"
                    chat_name = user.full_name if user else "Ошибка"
                    quote = html.quote(chat_name) if chat_name else chat_name

                    if chat_id in new_chats:
                        bot_logger.info(f"USER: {admin_id} | Новый чат {chat_id} @{username} | {chat_name}")
                        await create_dump_chat_user(admin_id, chat_id)
                        log_new.append(get_user_log_text(1, chat_id, username, quote))
                    else:
                        bot_logger.info(f"USER: {admin_id} | Удаленный чат {chat_id} @{username} | {chat_name}")
                        await del_dump_chat_user(admin_id, chat_id)
                        log_del.append(get_user_log_text(2, chat_id, username, quote))

                settings = await get_account_tg_to_user_id(admin_id)

                if settings.alert_new_chat:
                    target_id = settings.admin_id if settings.alert_new_chat_id < 10 else settings.alert_new_chat_id
                    for text_chunk in chunk_text(log_new):
                        await bot.send_message(target_id, text_chunk)

                if settings.alert_del_chat:
                    target_id = settings.admin_id if settings.alert_del_chat_id < 10 else settings.alert_del_chat_id
                    for text_chunk in chunk_text(log_del):
                        await bot.send_message(target_id, text_chunk)

            except Exception:
                bot_logger.error(traceback.format_exc())

    except Exception:
        bot_logger.error(traceback.format_exc())


async def starting_tg_parse_dialogs_handler():
    bot_logger.debug("starting tg_parse_dialogs_handler")
    await __tg_parse_dialogs_handler()
    scheduler.start()
