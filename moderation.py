from config import cfg
from storage import add_warning, get_warnings, reset_warnings
from filters import has_profanity, contains_link

async def handle_moderation(ctx: dict, msg: dict):
    """
    ctx = {"client", "chat_id", "user_id", "username"}
    msg = {"message_id", "text", "chat_type"}
    """
    chat_type = msg.get("chat_type")
    if chat_type not in ("group", "supergroup"):
        return  # فقط گروه

    text = msg.get("text") or ""
    reason = None

    if cfg.enable_anti_profanity and has_profanity(text):
        reason = "استفاده از کلمات نامناسب"

    if not reason and cfg.enable_anti_link and contains_link(text):
        reason = "ارسال لینک ممنوع"

    if not reason:
        return

    # حذف پیام (نیازمند پیاده‌سازی در client)
    try:
        await ctx["client"].delete_message(ctx["chat_id"], msg.get("message_id"))
    except Exception:
        pass

    warns = await add_warning(ctx["user_id"], ctx["chat_id"], 1)
    user_display = f"@{ctx['username']}" if ctx.get("username") else f"{ctx['user_id']}"
    warn_text = f"کاربر {user_display} اخطار {warns} از {cfg.max_warnings} — {reason}"

    try:
        await ctx["client"].send_message(ctx["chat_id"], warn_text)
    except Exception:
        pass

    if warns >= cfg.max_warnings:
        # حذف عضو (نیازمند پیاده‌سازی در client)
        try:
            await ctx["client"].kick_member(ctx["chat_id"], ctx["user_id"])
            await ctx["client"].send_message(ctx["chat_id"], f"کاربر {user_display} به دلیل ۵ اخطار حذف شد.")
        except Exception:
            pass
        await reset_warnings(ctx["user_id"], ctx["chat_id"])
