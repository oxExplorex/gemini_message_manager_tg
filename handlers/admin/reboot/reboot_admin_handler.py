import os

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import data.text as constant_text
from filters.all_filters import IsAdmin, IsPrivate
from loader import router, apps_session
from utils.updating_utils.update_bot import download_and_extract_github_repo


# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), F.text.in_(constant_text.RESTART_BOT_W_KEYBOARD), StateFilter("*"))
async def restart_admin_handler(message: Message, state: FSMContext):
    await state.clear()

    await message.answer("Перезапускаю...")

    for app in apps_session:
        if app.is_initialized:
            await app.stop()

    await download_and_extract_github_repo()

    os.system("start.bat")


# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), F.text.in_(constant_text.RESTART_BOT_U_KEYBOARD), StateFilter("*"))
async def restart_admin_handler(message: Message, state: FSMContext):
    await state.clear()

    return await message.answer("Разработка :)")

    for app in apps_session:
        if app.is_initialized:
            await app.stop()

    os.system("start.bat")