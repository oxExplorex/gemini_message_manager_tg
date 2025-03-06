
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder




def back_inline():
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        InlineKeyboardButton(
            text=f"Отмена",
            callback_data=f"back_delete"
        ),
    )
    return keyboard.as_markup()


