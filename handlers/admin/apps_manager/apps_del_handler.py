import os

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.main import get_app_tg_user_id, get_app_tg_to_params_all, create_app_tg, get_app_tg_uuid, del_app_tg_uuid
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.agree_inline import agree_inline
from keyboards.inline.apps_manager.apps_menu_inline import apps_tg_admin_inline
from keyboards.inline.back_inline import back_inline
from loader import router, apps_session

import data.text as constant_text
from utils.others import not_warning_delete_message


@router.callback_query(IsPrivate(), IsAdmin(), F.data.startswith("apps_admin_menu_delete:"), StateFilter("*"))
async def apps_del_app_tg_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    uuid_app_tg = call.data.split(":")[1]
    _user_id = call.from_user.id

    if await del_app_tg_uuid(uuid_app_tg, _user_id):
        return await call.message.answer(constant_text.SUCCESS_DEL_APP_TEXT)

    return await call.answer(constant_text.ERROR_DEL_APP_TEXT)


