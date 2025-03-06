import os

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.main import get_app_tg_user_id
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.apps_manager.apps_menu_inline import apps_tg_admin_inline
from loader import router, apps_session

import data.text as constant_text
from utils.datetime_tools import DateTime


#
async def _get_apps_tg(user_id, offset):
    _apps_tg, _count = await get_app_tg_user_id(user_id, offset)
    if not _apps_tg:
        return [0, await apps_tg_admin_inline(_apps_tg, offset, _count)]

    return [_count, await apps_tg_admin_inline(_apps_tg, offset, _count)]


# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), F.text.in_(constant_text.APP_TG_USER_KEYBOARD), StateFilter("*"))
async def apps_menu_handler(message: Message, state: FSMContext):
    await state.clear()

    _user_id = message.from_user.id

    _count, _reply_keyboard = await _get_apps_tg(_user_id, 0)

    await message.answer(
        text=constant_text.APPS_COUNT_INFO_TEXT.format(
            _count=_count,
            date=DateTime().time_strftime("%d.%m.%Y %H:%M:%S.%f")),
        reply_markup=_reply_keyboard)


@router.callback_query(IsPrivate(), IsAdmin(), F.data.startswith("apps_admin_menu:"), StateFilter("*"))
async def apps_menu_offset_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    _offset = int(call.data.split(":")[-1])
    _user_id = call.from_user.id

    if _offset < 0:
        return await call.answer(constant_text.WARNING_NOT_ACCOUNT_ANSWER)

    _count, _reply_keyboard = await _get_apps_tg(_user_id, _offset)


    await call.message.edit_text(
        text=constant_text.APPS_COUNT_INFO_TEXT.format(
            _count=_count,
            date=DateTime().time_strftime("%d.%m.%Y %H:%M:%S.%f")),
        reply_markup=_reply_keyboard
    )
