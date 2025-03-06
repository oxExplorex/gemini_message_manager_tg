from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import data.text as constant_text

from filters.all_filters import IsPrivate, IsAdmin
from keyboards.main.start_keyboard import static_admin_keyboard
from loader import router


@router.message(IsPrivate(), IsAdmin(), F.text.startswith("/start"), StateFilter("*"))
async def start_user_handler(message: Message, state: FSMContext):
    await state.clear()

    version = None
    version_status = None
    last_check = None
    last_check_sec = None

    await message.answer(
        text=constant_text.START_MESSAGE_TEXT.format(
            version=version,
            version_status=version_status,
            last_check=last_check,  #
            last_check_sec=last_check_sec,  #
        ),
        reply_markup=static_admin_keyboard()
    )