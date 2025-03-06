import os

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from db.main import get_app_tg_user_id, get_app_tg_to_params_all, create_app_tg
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.agree_inline import agree_inline
from keyboards.inline.apps_manager.apps_menu_inline import apps_tg_admin_inline
from keyboards.inline.back_inline import back_inline
from loader import router, apps_session

import data.text as constant_text
from utils.others import not_warning_delete_message


@router.callback_query(IsPrivate(), IsAdmin(), F.data == "apps_admin_menu_add", StateFilter("*"))
async def apps_add_app_tg_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    _mess = await call.message.answer(
        text=constant_text.APPS_ADD_APP_ID_TEXT,
        reply_markup=back_inline(),
    )

    await state.update_data(_mess=_mess,)
    await state.set_state("apps_add_app_id")


@router.message(IsPrivate(), IsAdmin(), StateFilter("apps_add_app_id"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    _user_id = message.from_user.id

    await not_warning_delete_message(message=data['_mess'])

    _error = False
    try:
        _app_id = int(message.text)
    except:
        _app_id = 0
        _error = True

    if _error or _app_id <= 0:
        await state.clear()
        return await message.answer(
            text=constant_text.ERROR_FORMAT_TEXT,
        )

    _mess = await message.answer(
        text=constant_text.APPS_ADD_API_HASH_TEXT,
        reply_markup=back_inline(),
    )

    await state.update_data(_mess=_mess, _app_id=_app_id)
    await state.set_state("apps_add_api_hash")


@router.message(IsPrivate(), IsAdmin(), StateFilter("apps_add_api_hash"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    _user_id = message.from_user.id

    await not_warning_delete_message(message=data['_mess'])

    _api_hash = message.text

    _mess = await message.answer(
        text=constant_text.APPS_ADD_NAME_TAG_TEXT,
        reply_markup=back_inline(),
    )

    await state.update_data(_mess=_mess, _api_hash=_api_hash)
    await state.set_state("apps_add_tag_name")


@router.message(IsPrivate(), IsAdmin(), StateFilter("apps_add_tag_name"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    _user_id = message.from_user.id

    await not_warning_delete_message(message=data['_mess'])

    _tag_name = message.text

    _mess = await message.answer(
        text=constant_text.APPS_ADD_AGREE_TEXT.format(
            _app_id=data['_app_id'],
            _api_hash=data['_api_hash'],
            _tag_name=_tag_name,
        ),
        reply_markup=agree_inline(),
    )

    await state.update_data(_tag_name=_tag_name)
    await state.set_state("apps_add_agree")


@router.callback_query(IsPrivate(), IsAdmin(), F.data == "agree", StateFilter("apps_add_agree"))
async def apps_add_app_tg_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.clear()

    _user_id = call.from_user.id

    _app_id = data['_app_id']
    _api_hash = data['_api_hash']
    _tag_name = data['_tag_name']

    if await get_app_tg_to_params_all(user_id=_user_id, app_id=_app_id, api_hash=_api_hash):
        return await call.message.edit_text(
            text=constant_text.ERROR_ALREADY_APP_TEXT
        )

    await create_app_tg(
        user_id=_user_id,
        app_id=_app_id,
        api_hash=_api_hash,
        tag_name=_tag_name
    )

    return await call.message.edit_text(
        text=constant_text.SUCCESS_ADD_APP_TEXT
    )

