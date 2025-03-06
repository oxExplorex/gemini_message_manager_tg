EMOJI_YES_OR_NO_TEXT = ["❌", "✅"]

# text
START_MESSAGE_TEXT = "Панелька для самых лучших\n\n"\
                     "Version: <code>{version}</code> ({version_status})\n\n"\
                     "Last Check: <code>{last_check}</code> (~<code>{last_check_sec}</code> sec)\n"
NOTICE_ADMINISTRATOR_TO_ACTIVE_BOT = "Бот запущен"

APPS_COUNT_INFO_TEXT = "Всего приложений: {_count}\n\n<code>{date}</code>"
ACCOUNT_COUNT_INFO_TEXT = "<b>Добавление аккаунтов через Apps.</b>\n\nАккаунты: {_count}\nПриложений: {_count_apps}\n\n\n<code>{date}</code>"

ACCOUNT_EDIT_INFO_TEXT = "<b>Настройка аккаунта [<code>{user_id}</code>]</b>\n\n"\
                         "Телефон: <code>{number}</code>\n\n"\
                         "app_id: <code>{app_id}</code>\n"\
                         "api_hash: <code>{api_hash}</code>\n\n"\
                         "Последний актив: {last_update}\n\n"\
                         "<code>{date}</code>"


APPS_ADD_APP_ID_TEXT = "Введите app_id"
APPS_ADD_API_HASH_TEXT = "Введите api_hash"
APPS_ADD_NAME_TAG_TEXT = "Введите tag, чтобы отличать его от других приложений"
APPS_ADD_AGREE_TEXT = "Проверьте данные перед сохранением\n\n"\
                      "TAG: <b>{_tag_name}</b>\n"\
                      "APP_ID: <code>{_app_id}</code>\n"\
                      "API_HASH: <code>{_api_hash}</code>"\

ACCOUNT_CHOICE_APP_ID_TEXT = "Выберите приложение для продолжения"
ACCOUNT_INPUT_NUMBER_TEXT = "Напишите номер в формате +79001112233 или 79001112233"
ACCOUNT_INPUT_CODE_TEXT = "Введите код, который прислал вам тг (Если у вас не входит, попробуйте написать код .1.2.3.4.5.6 )"
ACCOUNT_INPUT_PASSWORD_TEXT = "Введите облачный пароль"

# WARN Error
WARNING_NOT_APP_TG_ANSWER = "⚠️ Выход за пределы списка"
WARNING_NOT_APP_TG_ANSWER = "⚠️ Нет ни одного приложения."

WARNING_NOT_ACCOUNT_ANSWER = "⚠️ Нет ни одного аккаунта."

WARNING_NOT_APP_TG = "⚠️ WARNING ⚠️\n\n"\
                     "️У вас нет приложения.\n"\
                     "Нужно добавить хотя бы одно через \"<code>{APP_TG_BUTTON}</code>\""
# ERROR
ERROR_FORMAT_TEXT = "⚠️ Неверный формат"
ERROR_ALREADY_APP_TEXT = "Приложение уже добавлено"
ERROR_DEL_APP_TEXT = "Приложения не существует."
ERROR_NOT_FOUND_APP_ID = "Приложение не найдено"
ERROR_NOT_FOUND_ACCOUNT_ID = "Аккаунт не найден"

# SUCCESS
SUCCESS_ADD_APP_TEXT = "✅ Успешно добавил приложение."
SUCCESS_DEL_APP_TEXT = "✅ Успешно удалил приложение."
SUCCESS_ADD_ACCOUNT_TEXT = "✅ Успешно добавил аккаунт\n\n"\
                           "Важные шаги:\n"\
                           "⚙️ <b>Настроить</b> сессию (Не обязательно)\n"\
                           "⚙️ ⚠️ <b>Перезапустить</b> бота (Обязательно)\n"\



# keyboards
ACCOUNTS_USER_KEYBOARD = [
    "📄 Accounts",
]
APP_TG_USER_KEYBOARD = [
    "🈸 Apps",
]
PROXY_USER_KEYBOARD = [
    "🌐 Proxy",
]
SETTINGS_BOT_KEYBOARD = [
    "⚙️ Настройки",
]
RESTART_BOT_W_KEYBOARD = [
    "🔄 ReBoot (Win)",
]
RESTART_BOT_U_KEYBOARD = [
    "🔄 (Dev) ReBoot (Ubuntu)",
]

