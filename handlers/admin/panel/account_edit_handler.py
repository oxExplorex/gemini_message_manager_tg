import os
import traceback

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded

import data.text as constant_text
from _logging import bot_logger
from db.main import get_app_tg_uuid, create_account_tg, update_user, get_account_uuid
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.account_managet.account_edit_inline import account_edit_admin_inline
from keyboards.inline.back_inline import back_inline
from loader import router
from utils.datetime_tools import DateTime
from utils.others import not_warning_delete_message


@router.callback_query(IsPrivate(), IsAdmin(), F.data.startswith("account_admin_menu_edit:"), StateFilter("*"))
async def accounts_edit_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    _user_id = call.from_user.id
    uuid_account = call.data.split(":")[-1]

    _account = await get_account_uuid(uuid_account, _user_id)

    if not _account:
        return await call.answer(constant_text.ERROR_NOT_FOUND_ACCOUNT_ID)

    number = _account.number
    app_uuid = _account.app_tg

    _app_tg = await get_app_tg_uuid(app_uuid, _user_id)
    if not _app_tg:
        return await call.answer(constant_text.ERROR_NOT_FOUND_APP_ID)

    app_id = _app_tg.app_id
    api_hash = _app_tg.api_hash

    await call.message.edit_text(
        text=constant_text.ACCOUNT_EDIT_INFO_TEXT.format(
            user_id=_account.user_id,

            number=number,

            app_id=app_id,
            api_hash=api_hash,

            last_update=_account.last_update,

            date=DateTime().time_strftime("%d.%m.%Y %H:%M:%S.%f"),
        ),
        reply_markup=await account_edit_admin_inline(_account),
    )
