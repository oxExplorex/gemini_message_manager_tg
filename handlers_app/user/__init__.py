from .gemini_handler import gemini_app_handler

router_app = [gemini_app_handler]

__all__ = ["router_app"]
