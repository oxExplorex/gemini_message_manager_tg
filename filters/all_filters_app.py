from pyrogram import filters
from pyrogram.types import Message


def file_with_spoiler_or_ttl(_, __, message: Message):
    if message.photo:
        return message.photo.has_spoiler or message.photo.ttl_seconds
    if message.video:
        return message.video.ttl_seconds
    if message.video_note:
        return message.video_note.ttl_seconds
    return False


file_spoiler_filter = filters.create(file_with_spoiler_or_ttl)