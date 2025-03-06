
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder




def agree_inline():
    keyboard = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text=f"✅ Подтвердить",
            callback_data=f"agree"
        ),
    )
    keyboard.row(
        InlineKeyboardButton(
            text=f"Отмена",
            callback_data=f"back_delete"
        ),
    )
    return keyboard.as_markup()


