import re

# لیست کلمات رکیک (از پیام شما)
BAD_WORDS = {
    "کیر","کص","کس","کسکش","کصکش","کثکش","کسخل","کصخل","کثخل",
    "کیرم","کیرت","کیرش","کون","کونت","کونم","کونکش",
    "گاییدن","گاییدم","گایید","جنده","مادرسگ","پدرسگ","گوه","رید","ریدم","ریدی","ریدین"
}

LINK_RE = re.compile(r'(https?://\S+|www\.\S+|t\.me/\S+|rubika\.\S+)', re.IGNORECASE)

def normalize(text: str) -> str:
    t = text.strip().lower()
    t = t.replace("ي","ی").replace("ك","ک")
    t = t.replace("\u200c", "")  # حذف نیم‌فاصله
    t = t.replace("_", " ")
    return t

def has_profanity(text: str) -> bool:
    t = normalize(text)
    for w in BAD_WORDS:
        if w in t:
            return True
    return False

def contains_link(text: str) -> bool:
    return bool(LINK_RE.search(text or ""))
