import traceback

import google.generativeai as genai
from pyrogram import Client
from pyrogram.types import Message

from _logging import bot_logger
from loader import chat_gemini


async def reply_post_handler(client: Client, message: Message):
    if (await client.get_me()).id != message.from_user.id:
        return

    try:
        await message.delete()
    except:
        bot_logger.error(traceback.format_exc())

    url = message.text.split(".p")[-1]

    chat_id = url.split("t.me/")[-1].split("/")[0]
    message_id = url.split("/")[-1]

    if "http" in url:
        try:
            await client.forward_messages(
                chat_id=message.chat.id,
                from_chat_id=chat_id,
                message_ids=int(message_id)
            )
        except:
            bot_logger.error(traceback.format_exc())
