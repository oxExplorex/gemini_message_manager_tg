import traceback

from pyrogram import Client
from pyrogram.types import Message

from _logging import bot_logger


async def reply_post_handler(client: Client, message: Message):
    if (await client.get_me()).id != message.from_user.id:
        return

    try:
        # Получаем текст команды без префикса "+ "
        text = message.text.strip()

        # Проверяем, что это URL Telegram
        if "t.me/" not in text:
            bot_logger.warning(f"Invalid URL format: {text}")
            return

        # Удаляем сообщение
        await message.delete()

        # Парсим URL
        # Формат: t.me/channel/123 или t.me/c/123456/123
        url_part = text.split("t.me/")[-1]
        parts = url_part.split("/")

        if len(parts) < 2:
            bot_logger.error(f"Invalid URL structure: {text}")
            return

        # Если это приватный канал (t.me/c/...)
        if parts[0] == "c" and len(parts) >= 3:
            chat_id = f"-100{parts[1]}"  # Добавляем префикс для приватных каналов
            message_id = int(parts[2])
        else:
            # Публичный канал
            chat_id = parts[0] if not parts[0].startswith("@") else parts[0]
            message_id = int(parts[1])

        # Форвардим сообщение
        await client.forward_messages(
            chat_id=message.chat.id,
            from_chat_id=chat_id,
            message_ids=message_id
        )

    except ValueError as e:
        bot_logger.error(f"Invalid message ID format: {e}")
    except Exception as e:
        bot_logger.error(f"Error in reply_post_handler: {traceback.format_exc()}")