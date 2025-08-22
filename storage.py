import aiosqlite
from typing import Optional, Tuple

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            first_seen_ts INTEGER,
            banned INTEGER DEFAULT 0
        )""")
        await db.execute("""
        CREATE TABLE IF NOT EXISTS warnings(
            user_id INTEGER,
            chat_id INTEGER,
            warns INTEGER DEFAULT 0,
            PRIMARY KEY(user_id, chat_id)
        )""")
        await db.commit()

async def upsert_user(user_id: int, ts: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        INSERT INTO users(user_id, first_seen_ts) VALUES(?, ?)
        ON CONFLICT(user_id) DO NOTHING
        """, (user_id, ts))
        await db.commit()

async def set_ban(user_id: int, banned: bool):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET banned=? WHERE user_id=?", (1 if banned else 0, user_id))
        await db.commit()

async def is_banned(user_id: int) -> bool:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT banned FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
            return bool(row[0]) if row else False

async def list_users():
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users WHERE banned=0") as cur:
            return [r[0] for r in await cur.fetchall()]

# ——— مدیریت اخطارها ———
async def get_warnings(user_id: int, chat_id: int) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT warns FROM warnings WHERE user_id=? AND chat_id=?", (user_id, chat_id)) as cur:
            row = await cur.fetchone()
            return int(row[0]) if row else 0

async def add_warning(user_id: int, chat_id: int, delta: int = 1) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO warnings(user_id, chat_id, warns) VALUES(?, ?, 0)
            ON CONFLICT(user_id, chat_id) DO NOTHING
        """, (user_id, chat_id))
        await db.execute("UPDATE warnings SET warns = warns + ? WHERE user_id=? AND chat_id=?", (delta, user_id, chat_id))
        await db.commit()
    return await get_warnings(user_id, chat_id)

async def reset_warnings(user_id: int, chat_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE warnings SET warns=0 WHERE user_id=? AND chat_id=?", (user_id, chat_id))
        await db.commit()
