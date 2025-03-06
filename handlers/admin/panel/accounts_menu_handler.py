import os

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.main import get_app_tg_user_id, get_account_user_id
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.account_managet.account_menu_inline import account_tg_admin_inline
from loader import router, apps_session

import data.text as constant_text
from utils.datetime_tools import DateTime


async def _get_account_tg(user_id, offset):
    _apps_tg, _count = await get_account_user_id(user_id, offset)
    if not _apps_tg:
        return [0, await account_tg_admin_inline(_apps_tg, offset, _count)]

    return [_count, await account_tg_admin_inline(_apps_tg, offset, _count)]

# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), F.text.in_(constant_text.ACCOUNTS_USER_KEYBOARD), StateFilter("*"))
async def accounts_menu_handler(message: Message, state: FSMContext):
    await state.clear()

    _user_id = message.from_user.id

    _, _count_apps = await get_app_tg_user_id(_user_id)
    if not _count_apps:
        return await message.answer(
            constant_text.WARNING_NOT_APP_TG.format(
                APP_TG_BUTTON=constant_text.APP_TG_USER_KEYBOARD[0],
            )
        )

    _count, _reply_keyboard = await _get_account_tg(_user_id, 0)

    await message.answer(
        text=constant_text.ACCOUNT_COUNT_INFO_TEXT.format(
            _count=_count,
            _count_apps=_count_apps,
            date=DateTime().time_strftime("%d.%m.%Y %H:%M:%S.%f"),
        ),
        reply_markup=_reply_keyboard,
    )


@router.callback_query(IsPrivate(), IsAdmin(), F.data.startswith("account_admin_menu:"), StateFilter("*"))
async def account_menu_offset_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    _offset = int(call.data.split(":")[-1])
    _user_id = call.from_user.id

    if _offset < 0:
        return await call.answer(constant_text.WARNING_NOT_ACCOUNT_ANSWER)

    _, _count_apps = await get_app_tg_user_id(_user_id)
    _count, _reply_keyboard = await _get_account_tg(_user_id, _offset)


    await call.message.edit_text(
        text=constant_text.ACCOUNT_COUNT_INFO_TEXT.format(
            _count=_count,
            _count_apps=_count_apps,
            date=DateTime().time_strftime("%d.%m.%Y %H:%M:%S.%f"),
        ),
        reply_markup=_reply_keyboard,
    )