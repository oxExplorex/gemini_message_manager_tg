from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import data.text as constant_text
from filters.all_filters import IsAdmin, IsPrivate
from loader import router


# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), F.text.in_(constant_text.PROXY_USER_KEYBOARD), StateFilter("*"))
async def proxy_menu_handler(message: Message, state: FSMContext):
    await state.clear()

    _user_id = message.from_user.id

    await message.answer("В разработке")

