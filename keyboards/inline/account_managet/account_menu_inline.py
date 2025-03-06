from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.main import get_user
from db.models import apps_db


async def account_tg_admin_inline(account_tg: List[apps_db], offset, _count):
    keyboard = InlineKeyboardBuilder()

    for i in account_tg:
        _name = None
        _user = await get_user(i.user_id)
        if _user:
            _name = _user.full_name
        else:
            _name = None

        keyboard.row(
            InlineKeyboardButton(
                text=f"⚙️ {_name} [{i.user_id}]",
                callback_data=f"account_admin_menu_edit:{i.uuid}"
            ),
        )
    keyboard.row(
        InlineKeyboardButton(
            text=f"⬅️",
            callback_data=f"account_admin_menu:{offset - 5}"
        ),
        InlineKeyboardButton(
            text=f"{offset}/{_count}",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"➡️",
            callback_data=f"account_admin_menu:{offset + 5}"
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Обновить",
            callback_data=f"account_admin_menu:{offset}"
        ),
    )


    return keyboard.as_markup()




