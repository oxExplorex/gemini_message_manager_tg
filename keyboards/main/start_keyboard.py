from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

import data.text as constant_text

def static_admin_keyboard():
    keyboard = [
        [
            KeyboardButton(text=constant_text.ACCOUNTS_USER_KEYBOARD[0]),
        ],
        [
            KeyboardButton(text=constant_text.APP_TG_USER_KEYBOARD[0]),
            KeyboardButton(text=constant_text.PROXY_USER_KEYBOARD[0]),
        ],
        [
            KeyboardButton(text=constant_text.SETTINGS_BOT_KEYBOARD[0]),
        ],
        [
            KeyboardButton(text=constant_text.RESTART_BOT_W_KEYBOARD[0]),
            KeyboardButton(text=constant_text.RESTART_BOT_U_KEYBOARD[0]),
        ],
    ]

    menu_default = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Бесплатный менеджер от Рыжика (lolz.live)"
    )
    return menu_default




