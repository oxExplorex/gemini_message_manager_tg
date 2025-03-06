from .errors import router

from .admin import router

from .user import router  # Тут юзеры


__all__ = ["router"]
