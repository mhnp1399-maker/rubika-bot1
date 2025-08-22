import time
from rate_limit import RateLimiter
from storage import upsert_user, is_banned
from handlers import handle_start, handle_help, handle_ping, handle_broadcast
from config import cfg
from moderation import handle_moderation

rl = RateLimiter(cfg.rate_limit_per_user_per_min)

def _chat_type(chat: dict) -> str:
    # بسته به ساختار روبیکا این را تطبیق دهید
    # مثال‌های ممکن: "private", "group", "supergroup"
    return chat.get("type") or "private"

async def route_update(update, client):
    # ساختار زیر را مطابق روبیکا تنظیم کنید
    msg = update.get("message") or {}
    chat = msg.get("chat") or {}
    user = msg.get("from") or {}

    text = msg.get("text") or ""
    chat_id = chat.get("id")
    chat_type = _chat_type(chat)
    user_id = user.get("id")
    username = user.get("username")  # اگر وجود ندارد، خالی می‌ماند
    message_id = msg.get("message_id")

    if not chat_id or not user_id:
        return

    await upsert_user(user_id, int(time.time()))
    if await is_banned(user_id):
        return

    # محدودکننده
    if not rl.allow(user_id):
        return await client.send_message(chat_id, "لطفاً آهسته‌تر!")

    ctx = {
        "client": client,
        "chat_id": chat_id,
        "user_id": user_id,
        "username": username
    }

    # خوشامدگویی به عضو جدید (ساختار را با روبیکا هماهنگ کنید)
    new_member = msg.get("new_chat_member")
    if new_member:
        name = new_member.get("username") or new_member.get("first_name") or "دوست عزیز"
        try:
            await client.send_message(chat_id, cfg.welcome_text.format(name=name))
        except Exception:
            pass
        return

    # ضداسپم گروه (فحش/لینک) — قبل از پردازش کامندها
    await handle_moderation(ctx, {"message_id": message_id, "text": text, "chat_type": chat_type})

    # دستورات
    if text.startswith("/start"):
        return await handle_start(ctx)
    if text.startswith("/help"):
        return await handle_help(ctx)
    if text.startswith("/ping"):
        return await handle_ping(ctx)
    if text.startswith("/broadcast"):
        return await handle_broadcast(ctx, text.partition(" ")[2])
