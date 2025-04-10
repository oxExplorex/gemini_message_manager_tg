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

    await message.answer("Введите прокси для работы с gemini\n\nФормат:\n{ip}:{port}:{user}:{password} Или 0 для отключения")
    await state.set_state("wait_proxy_manager")


# DOES NOTHING
@router.message(IsPrivate(), IsAdmin(), StateFilter("wait_proxy_manager"))
async def proxy_menu_handler(message: Message, state: FSMContext):
    await state.clear()

    if message.text.count(":") == 3:
        _ip, _port, _user, _password = message.text.split(":")

        with open("data/proxy.txt", "w") as file:
            file.write(f"{_ip}:{_port}:{_user}:{_password}")

        return await message.answer("Прокси установлены")
    elif message.text == "0":

        with open("data/proxy.txt", "w") as file:
            file.write(f"0")

        return await message.answer("Прокси выключены")

    return await message.answer("Неверный формат прокси")







