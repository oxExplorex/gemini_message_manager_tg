import traceback

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import html

from _logging import bot_logger
from db.main import get_dump_chat_admin_all, update_user, get_user, create_dump_chat_user, del_dump_chat_user, \
    get_account_tg_to_user_id
from loader import apps_session, bot
from utils.others import get_user_log_text

scheduler = AsyncIOScheduler()


def _add_log(_list_log, _text):

    if not _list_log:
        _list_log.append("")

    if len(_list_log[-1]) >= 3500:
        _list_log.append("")

    _list_log[-1] += _text
    return


@scheduler.scheduled_job('interval', minutes=20)
async def __tg_parse_dialogs_handler():
    try:
        if apps_session is None:
            return bot_logger.error("apps_session is None")

        for app_session in apps_session:
            try:
                admin_id = (await app_session.get_me()).id

                last_check_chat_id = [x.chat_id for x in await get_dump_chat_admin_all(admin_id)]

                count_dialogs = await app_session.get_dialogs_count(pinned_only=None, chat_list=0)
                count_dialogs = await app_session.get_dialogs_count(pinned_only=None, chat_list=1) + count_dialogs

                parse_list = []
                new_chat = []

                _list_log = []
                _list_log_del = []

                bot_logger.info(f'START USER: {admin_id} | {count_dialogs}')
                async for x in app_session.get_dialogs(limit=count_dialogs + 10, pinned_only=True,
                                                       chat_list=None):  # chat_list - 0 Main | 1 Archive | None All
                    chat_id = x.chat.id
                    username = x.chat.username
                    chat_name = x.chat.full_name or x.chat.title

                    if chat_id not in last_check_chat_id and chat_id not in parse_list:
                        new_chat.append(chat_id)

                    if chat_id in parse_list:
                        pass
                    else:
                        parse_list.append(chat_id)

                        await update_user(chat_id, username, chat_name)


                # обрабатываем новые чаты и удаленные
                _temp = [x for x in last_check_chat_id if x not in parse_list + new_chat]
                for _chat_id in new_chat + _temp:
                    _user = await get_user(_chat_id)
                    if not _user:
                        username = "Ошибка"
                        chat_name = "Ошибка"
                    else:
                        username = _user.username
                        chat_name = _user.full_name

                    if _chat_id in new_chat:
                        bot_logger.info(f"USER: {admin_id} | Новый чат {_chat_id} @{username} | {chat_name}")
                        await create_dump_chat_user(admin_id, _chat_id)

                        _quote = html.quote(chat_name) if chat_name else chat_name
                        _add_log(_list_log, get_user_log_text(1, _chat_id, username, _quote))
                    else:
                        bot_logger.info(f"USER: {admin_id} | Удаленный чат {_chat_id} @{username} | {chat_name}")
                        await del_dump_chat_user(admin_id, _chat_id)

                        _quote = html.quote(chat_name) if chat_name else chat_name
                        _add_log(_list_log_del, get_user_log_text(2, _chat_id, username, _quote))

                _settings = await get_account_tg_to_user_id(admin_id)
                if _settings.alert_new_chat:
                    _log_chat_id = _settings.admin_id if _settings.alert_new_chat_id < 10 else _settings.alert_new_chat_id
                    for _text in _list_log:
                        await bot.send_message(_log_chat_id, _text)

                if _settings.alert_del_chat:
                    _log_chat_id = _settings.admin_id if _settings.alert_del_chat_id < 10 else _settings.alert_del_chat_id
                    for _text in _list_log_del:
                        await bot.send_message(_log_chat_id, _text)

            except Exception as e:
                bot_logger.error(traceback.format_exc())

    except:
        bot_logger.error(traceback.format_exc())


async def starting_tg_parse_dialogs_handler():
    bot_logger.debug("starting tg_parse_dialogs_handler")
    await __tg_parse_dialogs_handler()
    scheduler.start()
