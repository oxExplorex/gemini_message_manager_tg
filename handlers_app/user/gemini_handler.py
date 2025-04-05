
import google.generativeai as genai
from pyrogram import Client
from pyrogram.types import Message

from _logging import bot_logger
from loader import chat_gemini


def get_answer_text_list(_promt, question, answer):
    _temp = []

    _temp_str = f"Токены: {answer.usage_metadata.prompt_token_count} | {answer.usage_metadata.candidates_token_count} | {answer.usage_metadata.total_token_count}\n\n"
    _temp_str += f"<emoji id=5276507609652802495>👀</emoji> Промт: {_promt}\n\n" if _promt else ""
    _temp_str += f"<emoji id=5206479194388713063>❓</emoji> Вопрос: {question}\n\n" if question else ""
    _temp_str += f"<emoji id=5370939500811791703>🤓</emoji> Ответ: {answer.text}"
    _temp_str = f"{answer.text.replace("\\n", "\n")}"
    return _temp_str


def get_answer_text_pre(_repl):
    if _repl:
        if _repl.animation or _repl.video or _repl.video_note or (_repl.sticker and _repl.sticker.is_video):
            _temp_str = "<emoji id=5226906660143904201>🤨</emoji> Смотрю видео, подожди <emoji id=5220046725493828505>✍️</emoji>"
        elif _repl.voice or _repl.audio:
            _temp_str = "<emoji id=5226906660143904201>🤨</emoji> Слушаю голосовое, подожди <emoji id=5220046725493828505>✍️</emoji>"
        elif _repl.sticker:
            _temp_str = "<emoji id=5226906660143904201>🤨</emoji> Рассматриваю стикер, подожди <emoji id=5220046725493828505>✍️</emoji>"
        elif _repl.photo:
            _temp_str = "<emoji id=5226906660143904201>🤨</emoji> Рассматриваю фото, подожди <emoji id=5220046725493828505>✍️</emoji>"
        else:
            _temp_str = "<emoji id=5269436882302811645>👀</emoji> Думаю над чем-то непонятным, подожди <emoji id=5220046725493828505>✍️</emoji>"
    else:
        _temp_str = "<emoji id=5269436882302811645>👀</emoji> Думаю над текстом, подожди <emoji id=5220046725493828505>✍️</emoji>"
    return _temp_str


def _get_mime_type(_repl):
    if _repl:
        if _repl.animation or _repl.video or _repl.video_note or (_repl.sticker and _repl.sticker.is_video):
            return 'video/mp4'
        elif _repl.voice or _repl.audio:
            return "audio/wav"
        elif _repl.photo or _repl.sticker:
            return "image/png"
    return None

def _protos(_text, message: Message, _mime_type):
    # Так, делаем
    if _mime_type:
        return f"[Сообщение от @{message.from_user.username} ({message.from_user.id}) с вложением ниже |{message.from_user.full_name}] {_text}"
    return f"[Сообщение от @{message.from_user.username} ({message.from_user.id}) |{message.from_user.full_name}] {_text}"

async def gemini_app_handler(client: Client, message: Message):
    if (await client.get_me()).id != message.from_user.id:
        return

    _promt_root = (message.text or message.caption or "").replace(".", "", 1)
    _promt_reply = (message.reply_to_message.text or message.reply_to_message.caption or "") if message.reply_to_message else ""

    await message.edit_text(
        get_answer_text_pre(message.reply_to_message)
    )

    _mime_type = _get_mime_type(message.reply_to_message)
    if not(_mime_type is None) and message.reply_to_message:
        if _mime_type:
            pass
        else:
            return await message.edit_text("Я не знаю такой формат файла")

        animation = await message.reply_to_message.download(in_memory=True)

        _parts = [
            genai.protos.Part(text=_protos(_promt_root, message, None)) if _promt_root else None,
            genai.protos.Part(text=_protos(_promt_reply, message.reply_to_message, _mime_type)) if _promt_reply else None,
            genai.protos.Part(
                inline_data=genai.protos.Blob(
                    mime_type=_mime_type,
                    data=animation.getbuffer().tobytes()
                )
            )
        ]
        _parts = [i for i in _parts if i]

        response = await chat_gemini.send_message_async(
            content=genai.protos.Content(
                parts=_parts
            ),
        )
    else:
        _parts = [
            genai.protos.Part(text=_protos(_promt_root, message, None)) if _promt_root else genai.protos.Part(text="?"),
            genai.protos.Part(text=_protos(_promt_reply,  message.reply_to_message, None)) if _promt_reply else genai.protos.Part(text="?")
        ]

        response = await chat_gemini.send_message_async(
            content=genai.protos.Content(
                parts=_parts,
            ),
        )

    bot_logger.info(chat_gemini.history)

    await message.edit_text(
        text=get_answer_text_list(_promt_root, _promt_reply, response),
    )