import traceback
from typing import Union

import aiogram
from aiogram.types import Message, CallbackQuery

from _logging import bot_logger
from data.config import admin_id_list
from db.main import get_admins
import data.text as constant_text
from keyboards.main.start_keyboard import static_admin_keyboard
from loader import bot


async def send_log_to_active_bot(bot: aiogram.Bot):
    _admin_id_list = [
        x for x in set(
            admin_id_list + [x.user_id for x in await get_admins()]
        ) if x > 10
    ]
    for _admin_id in _admin_id_list:
        try:
            await bot.send_message(
                chat_id=_admin_id,
                text=constant_text.NOTICE_ADMINISTRATOR_TO_ACTIVE_BOT,
                reply_markup=static_admin_keyboard(),
            )
        except:
            pass

def get_user_log_text(action_id, _chat_id, username, _quote):

    _text = ""
    link_id = f'tg://user?id={_chat_id}'
    if action_id == 1:
        _text += f"💬 Обнаружен новый чат:\n  └  <code>{_chat_id}</code> {link_id} | @{username} | {_quote}\n"
    elif action_id == 2:
        _text += f"❗️ Хуесос удалил чат:\n  └  <code>{_chat_id}</code> {link_id} | @{username} | {_quote}\n"
    else:
        _text = "error?"
    return _text


async def not_warning_delete_message(chat_id: int = None, message_id: int = None, message: Union[CallbackQuery, Message] = None) -> bool:
    if not(message is None):
        if isinstance(message, Message):
            chat_id = message.chat.id
            message_id = message.message_id
        else:
            chat_id = message.message.chat.id
            message_id = message.message.message_id

    if not(chat_id is None) and not(message_id is None):
        while 1:
            try:
                await bot.delete_message(chat_id, message_id)
                return True
            except:
                bot_logger.error(traceback.format_exc())
                return False
    return False