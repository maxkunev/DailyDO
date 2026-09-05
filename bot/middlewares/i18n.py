from pathlib import Path
from typing import Any

from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.utils.i18n import I18n
from aiogram.utils.i18n.middleware import I18nMiddleware

from bot.services import get_user_language  

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"

i18n = I18n(
    path=LOCALES_DIR,
    default_locale="en",
    domain="messages",
)


class DBI18nMiddleware(I18nMiddleware):
    async def get_locale(self, event: TelegramObject, data: dict[str, Any]) -> str:
        user_id = None

        if isinstance(event, Message) and event.from_user:
            user_id = event.from_user.id
        elif isinstance(event, CallbackQuery) and event.from_user:
            user_id = event.from_user.id

        if not user_id:
            return self.i18n.default_locale

        language = await get_user_language(user_id)

        if language in {"en", "ru", "uk"}:
            return language

        return self.i18n.default_locale
    
    def set_locale(self, locale: str) -> None:
        self.i18n.current_locale = locale
            
i18n_middleware = DBI18nMiddleware(i18n)