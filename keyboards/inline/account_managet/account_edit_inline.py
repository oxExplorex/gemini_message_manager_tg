from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db.models import apps_db
import data.text as constant_text


def _inline_keyboard_button(text="", data="", url=""):
    if url:
        return InlineKeyboardButton(
            text=text,
            url=url,
        )
    return InlineKeyboardButton(
        text=text,
        callback_data=data
    )


async def account_edit_admin_inline(_account: apps_db):
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=f"*Help",
            callback_data=f"123"
        ),
    )


    keyboard.row(
        InlineKeyboardButton(
            text=f"New chat:",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"{constant_text.EMOJI_YES_OR_NO_TEXT[_account.alert_new_chat]}",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"{_account.alert_new_chat_id}",
            callback_data=f"123"
        )
    )

    keyboard.row(
        InlineKeyboardButton(
            text=f"Del chat:",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"{constant_text.EMOJI_YES_OR_NO_TEXT[_account.alert_del_chat]}",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"{_account.alert_del_chat}",
            callback_data=f"123"
        )
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Bot/SG/Channel:",
            callback_data=f"123"
        ),
        InlineKeyboardButton(
            text=f"{constant_text.EMOJI_YES_OR_NO_TEXT[_account.alert_bot]}",
            callback_data=f"123"
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Назад",
            callback_data=f"account_admin_menu:0"
        ),
    )


    return keyboard.as_markup()




