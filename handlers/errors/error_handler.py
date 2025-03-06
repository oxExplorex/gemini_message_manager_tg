import traceback

from aiogram.exceptions import AiogramError, DetailedAiogramError, CallbackAnswerException, SceneException, \
    UnsupportedKeywordArgument, TelegramNetworkError, TelegramUnauthorizedError, TelegramRetryAfter, \
    TelegramMigrateToChat, TelegramBadRequest, TelegramNotFound, ClientDecodeError, TelegramEntityTooLarge, \
    RestartingTelegram, TelegramServerError, TelegramForbiddenError, TelegramConflictError, TelegramAPIError
from aiogram.types import ErrorEvent

from _logging import bot_logger
from loader import router



@router.error()
async def errors_handler(event: ErrorEvent):
    # Base exception for all aiogram errors.
    if isinstance(event.exception, AiogramError):
        bot_logger.exception(f"AiogramError: {event.exception}\nUpdate: {event.update}")
        return True

    # Base exception for all aiogram errors with detailed message.
    if isinstance(event.exception, DetailedAiogramError):
        bot_logger.exception(f"AiogramError: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception for callback answer.
    if isinstance(event.exception, CallbackAnswerException):
        bot_logger.exception(f"AiogramError: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception for scenes.
    if isinstance(event.exception, SceneException):
        bot_logger.exception(f"AiogramError: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when a keyword argument is passed as filters.
    if isinstance(event.exception, UnsupportedKeywordArgument):
        bot_logger.exception(f"AiogramError: {event.exception}\nUpdate: {event.update}")
        return True

    # Base exception for all Telegram API errors.
    if isinstance(event.exception, TelegramAPIError):
        bot_logger.exception(f"TelegramAPIError: {event.exception}\nUpdate: {event.update}")
        return True

    # Бот не авторизован
    if isinstance(event.exception, TelegramUnauthorizedError):
        bot_logger.exception(f"TelegramUnauthorizedError: {event.exception}\nUpdate: {event.update}")
        return True

    # Base exception for all Telegram network errors.
    if isinstance(event.exception, TelegramNetworkError):
        bot_logger.exception(f"TelegramNetworkError: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when flood control exceeds.
    if isinstance(event.exception, TelegramRetryAfter):
        bot_logger.exception(f"TelegramRetryAfter: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when chat has been migrated to a supergroup.
    if isinstance(event.exception, TelegramMigrateToChat):
        bot_logger.exception(f"TelegramMigrateToChat: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when request is malformed.
    if isinstance(event.exception, TelegramBadRequest):
        bot_logger.exception(f"TelegramBadRequest: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when chat, message, user, etc. not found.
    if isinstance(event.exception, TelegramNotFound):
        bot_logger.exception(f"TelegramNotFound: {event.exception}\nUpdate: {event.update}")
        return True


    # Exception raised when bot token is already used by another application in polling mode.
    if isinstance(event.exception, TelegramConflictError):
        bot_logger.exception(f"TelegramConflictError: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when bot token is invalid.
    if isinstance(event.exception, TelegramUnauthorizedError):
        bot_logger.exception(f"TelegramUnauthorizedError: {event.exception}\nUpdate: {event.update}")
        return True


    # Exception raised when bot is kicked from chat or etc.
    if isinstance(event.exception, TelegramForbiddenError):
        bot_logger.exception(f"TelegramForbiddenError: {event.exception}\nUpdate: {event.update}")
        return True


    # Exception raised when Telegram server returns 5xx error.
    if isinstance(event.exception, TelegramServerError):
        bot_logger.exception(f"TelegramServerError: {event.exception}\nUpdate: {event.update}")
        return True


    # Exception raised when Telegram server is restarting.
    if isinstance(event.exception, RestartingTelegram):
        bot_logger.exception(f"RestartingTelegram: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when you are trying to send a file that is too large.
    if isinstance(event.exception, TelegramEntityTooLarge):
        bot_logger.exception(f"TelegramEntityTooLarge: {event.exception}\nUpdate: {event.update}")
        return True

    # Exception raised when client can’t decode response. (Malformed response, etc.)
    if isinstance(event.exception, ClientDecodeError):
        bot_logger.exception(f"ClientDecodeError: {event.exception}\nUpdate: {event.update}")
        return True

    # Все прочие ошибки
    bot_logger.exception(f"Update: {event.exception}\nUpdate: {event.update}")
    bot_logger.error(traceback.format_exc())
