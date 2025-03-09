from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from _logging import bot_logger
from db.main import update_user, get_dump_chat_user, get_account_tg_to_user_id, create_dump_chat_user
from loader import router, bot
from aiogram import html

from utils.others import get_user_log_text


@router.business_message(
    F.media_group_id,
    F.content_type.in_([
        ContentType.VIDEO,
        ContentType.VIDEO_NOTE,
        ContentType.ANIMATION,
        ContentType.PHOTO,
    ]),
    StateFilter("*"))
async def any_message_media_handler(message: Message, state: FSMContext):
    # bot_logger.debug(message)
    pass


@router.business_message(StateFilter("*"))
async def any_message_media_handler(message: Message, state: FSMContext):
    _admin_id = (await bot.get_business_connection(message.business_connection_id)).user.id

    _chat_id = message.chat.id
    username = message.chat.username
    chat_name = message.chat.full_name or message.chat.title

    # bot_logger.debug(message)

    if not await get_dump_chat_user(_admin_id, _chat_id):

        bot_logger.info(f"USER: {_admin_id} | Новый чат {_chat_id} @{username} | {chat_name}")
        await create_dump_chat_user(_admin_id, _chat_id)

        _quote = html.quote(chat_name) if chat_name else chat_name

        _settings = await get_account_tg_to_user_id(_admin_id)
        if _settings.alert_new_chat:
            _log_chat_id = _settings.admin_id if _settings.alert_new_chat_id < 10 else _settings.alert_new_chat_id
            await bot.send_message(_log_chat_id, get_user_log_text(1, _chat_id, username, _quote))


