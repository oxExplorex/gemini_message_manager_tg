from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery
from aiogram.types import Message
from typing import Union

from data.config import admin_id_list
from db.main import get_admins



class ChatTypeFilter_example(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            return message.chat.type in self.chat_type


class CheckBusinessConnectionId(BaseFilter):  # [1]
    async def __call__(self, message: Message) -> bool:  # [3]
        _user_id = message.from_user.id
        return True


class IsPrivate(BaseFilter):  # [1]
    async def __call__(self, message: Message) -> bool:  # [3]
        type_message = message.message.chat.type if isinstance(message, CallbackQuery) else message.chat.type
        return ChatType.PRIVATE == type_message


class IsAdmin(BaseFilter):  # [1]
    async def __call__(self, message: Message) -> bool:  # [3]
        _user_id = message.from_user.id
        return _user_id in admin_id_list or _user_id in [x.user_id for x in await get_admins()]
