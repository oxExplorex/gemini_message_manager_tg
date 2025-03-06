import os
import re
import traceback

from aiogram import F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeExpired

import data.text as constant_text
from _logging import bot_logger
from db.main import get_app_tg_uuid, create_account_tg, update_user
from filters.all_filters import IsAdmin, IsPrivate
from keyboards.inline.back_inline import back_inline
from loader import router
from utils.others import not_warning_delete_message


@router.callback_query(IsPrivate(), IsAdmin(), F.data.startswith("account_admin_menu_add:"), StateFilter("*"))
async def accounts_add_menu_handler(call: CallbackQuery, state: FSMContext):
    await state.clear()

    _user_id = call.from_user.id
    uuid_app = call.data.split(":")[-1]

    _mess = await call.message.answer(
        text=constant_text.ACCOUNT_INPUT_NUMBER_TEXT,
        reply_markup=back_inline(),
    )

    await state.update_data(_mess=_mess, uuid_app=uuid_app)
    await state.set_state("account_add_number")


@router.message(IsPrivate(), IsAdmin(), StateFilter("account_add_number"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    _user_id = message.from_user.id
    await not_warning_delete_message(message=data['_mess'])

    _number = "".join(re.findall(r'\d+', message.text))

    _app_info = await get_app_tg_uuid(data['uuid_app'], _user_id)
    if not _app_info:
        await state.clear()
        return await message.answer(constant_text.ERROR_NOT_FOUND_APP_ID)

    try:
        os.remove(f"data/session/{_number}")
    except FileNotFoundError:
        pass

    _app_temp = Client(
        name=f"data/session/{_number}",
        phone_number=_number,
        api_id=_app_info.app_id,
        api_hash=_app_info.api_hash,
    )

    try:
        await _app_temp.connect()
        result = await _app_temp.send_code(phone_number=_number)
        await state.update_data(_app_temp=_app_temp, _number=_number, _phone_hash=result.phone_code_hash)
        _mess = await message.answer(constant_text.ACCOUNT_INPUT_CODE_TEXT)
        await state.update_data(_mess=_mess)
        await state.set_state("account_add_code")

    except Exception as e:
        bot_logger.error(traceback.format_exc())
        await state.clear()
        if _app_temp.is_connected:
            await _app_temp.disconnect()
        return await message.answer(f"Ошибка: {e}")


@router.message(IsPrivate(), IsAdmin(), StateFilter("account_add_code"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    _user_id = message.from_user.id
    await not_warning_delete_message(message=data['_mess'])


    try:
        code = "".join(re.findall(r'\d+', message.text))
    except ValueError:
        return await message.answer(constant_text.ERROR_FORMAT_TEXT)

    _app_info = await get_app_tg_uuid(data['uuid_app'], _user_id)
    if not _app_info:
        await state.clear()
        return await message.answer(constant_text.ERROR_NOT_FOUND_APP_ID)

    _number = data['_number']
    _phone_hash = data['_phone_hash']
    _app_temp = data['_app_temp']

    try:
        result = await _app_temp.sign_in(
            phone_number=_number,
            phone_code_hash=_phone_hash,
            phone_code=code,
        )
        bot_logger.info(result)
        await _app_temp.disconnect()
        await create_account_tg(_user_id, result.id, data['uuid_app'], data['_number'])
        await message.answer(constant_text.SUCCESS_ADD_ACCOUNT_TEXT)
        await state.clear()

    except SessionPasswordNeeded:
        await state.set_state("account_add_password")
        return await message.answer(constant_text.ACCOUNT_INPUT_PASSWORD_TEXT)

    except PhoneCodeExpired:
        await message.answer("Код авторизации истек. Введите номер телефона заново.")
        await state.set_state("account_add_number")

    except Exception as e:
        bot_logger.error(traceback.format_exc())
        if _app_temp.is_connected:
            await _app_temp.disconnect()
        await message.answer(f"Ошибка: {e}")
        await state.clear()

@router.message(IsPrivate(), IsAdmin(), StateFilter("account_add_password"))
async def apps_menu_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    _app_temp = data['_app_temp']
    _user_id = message.from_user.id
    _password = message.text

    try:
        result = await _app_temp.check_password(_password)
        await _app_temp.disconnect()
        await create_account_tg(_user_id, result.id, data['uuid_app'], data['_number'])
        await update_user(result.id, result.username, result.full_name)
        await message.answer(constant_text.SUCCESS_ADD_ACCOUNT_TEXT)
        await state.clear()
    except Exception as e:
        if _app_temp.is_connected:
            await _app_temp.disconnect()
        await message.answer(f"Ошибка: {e}")
        await state.clear()