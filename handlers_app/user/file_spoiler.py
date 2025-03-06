import pathlib

import google.generativeai as genai
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import Message

from data.config import admin_id_list, GEMINI_KEY


async def file_spoiler_handler(client: Client, message: Message):
    print(f"Временное сообщение: {message.text}")
    pass
