from typing import List

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import app_tg_db


async def apps_tg_admin_inline(apps_tg: List[app_tg_db], offset, _count):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=f"➕ Добавить приложение",
            callback_data=f"apps_admin_menu_add"
        ),
    )

    for i in apps_tg:
        # account_id | name | statusv1 | statusv2 | delete
        keyboard.row(
            InlineKeyboardButton(
                text=f"🔑 Add |  {i.tag_name} [{i.app_id}]",
                callback_data=f"account_admin_menu_add:{i.uuid}"
            ),
            InlineKeyboardButton(
                text=f"🗑 DEL",
                callback_data=f"apps_admin_menu_delete:{i.uuid}"
            ),
        )
    keyboard.row(
        InlineKeyboardButton(
            text=f"⬅️",
            callback_data=f"apps_admin_menu:{offset - 5}"
        ),
        InlineKeyboardButton(
            text=f"{offset}/{_count}",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"➡️",
            callback_data=f"apps_admin_menu:{offset + 5}"
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Обновить",
            callback_data=f"apps_admin_menu:{offset}"
        ),
    )


    return keyboard.as_markup()


