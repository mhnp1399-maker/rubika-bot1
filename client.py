import httpx
from typing import Any, Dict, List, Optional
from config import cfg

class RubikaClient:
    def __init__(self, token: str, base_url: str):
        self.base = base_url.rstrip("/")
        self.token = token
        self.http = httpx.AsyncClient(timeout=20)

    async def get_updates(self, offset: Optional[int] = None) -> List[Dict[str, Any]]:
        # TODO: با اندپوینت واقعی روبیکا جایگزین کنید
        return []

    async def send_message(self, chat_id: int, text: str, reply_to_id: Optional[int] = None):
        # TODO: پیاده‌سازی واقعی
        pass

    async def delete_message(self, chat_id: int, message_id: int):
        # TODO: پیاده‌سازی واقعی حذف پیام
        pass

    async def kick_member(self, chat_id: int, user_id: int):
        # TODO: پیاده‌سازی واقعی حذف عضو
        pass

    async def send_audio(self, chat_id: int, file_path: str, caption: Optional[str] = None):
        # TODO: پیاده‌سازی واقعی ارسال فایل/صوت
        pass

    async def close(self):
        await self.http.aclose()
