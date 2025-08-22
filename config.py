from pydantic import BaseModel
import os

class Config(BaseModel):
    api_base: str = os.getenv("RUBIKA_API_BASE", "https://api.rubika.example")
    bot_token: str = os.getenv("RUBIKA_BOT_TOKEN", "")
    admin_ids: list[int] = [int(x) for x in os.getenv("ADMIN_IDS", "123456789").split(",")]
    poll_interval: float = float(os.getenv("POLL_INTERVAL", "1.0"))
    rate_limit_per_user_per_min: int = int(os.getenv("RATE_LIMIT", "20"))

    # تنظیمات ضداسپم و خوشامدگویی
    enable_anti_profanity: bool = True
    enable_anti_link: bool = True
    max_warnings: int = 5
    welcome_text: str = "خوش اومدی {name}! قوانین گروه رو رعایت کن ✌️"

cfg = Config()
