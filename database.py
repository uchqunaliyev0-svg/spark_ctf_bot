kimport asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            university TEXT,
            experience_level TEXT,
            points INTEGER DEFAULT 0,
            tasks_solved INTEGER DEFAULT 0
        )
    ''')
    await conn.close()

async def add_user(user_id, full_name, university, experience_level):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO users (user_id, full_name, university, experience_level)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (user_id) DO UPDATE
        SET full_name = $2, university = $3, experience_level = $4
    ''', user_id, full_name, university, experience_level)
    await conn.close()

async def get_user(user_id):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
    await conn.close()
    return row

# MANA BU YANGI FUNKSIYA (Statistika uchun)
async def count_users():
    conn = await asyncpg.connect(DATABASE_URL)
    count = await conn.fetchval('SELECT COUNT(*) FROM users')
    await conn.close()
    return count
