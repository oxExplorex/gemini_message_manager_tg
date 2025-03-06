from aiogram import F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from _logging import bot_logger
from loader import router, bot
from aiogram import html


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
    bot_logger.debug(message)
    pass


@router.business_message(StateFilter("*"))
async def any_message_media_handler(message: Message, state: FSMContext):
    _user_id = (await bot.get_business_connection(message.business_connection_id)).user.id

    chat_id = message.chat.id
    username = message.chat.username
    chat_name = message.chat.full_name or message.chat.title

    bot_logger.debug(message)


