import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            nickname TEXT,
            points INTEGER DEFAULT 0,
            solved_count INTEGER DEFAULT 0
        )
    ''')
    await conn.close()

async def add_user(user_id, nickname):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO users (user_id, nickname)
        VALUES ($1, $2)
        ON CONFLICT (user_id) DO UPDATE SET nickname = $2
    ''', user_id, nickname)
    await conn.close()

async def get_user(user_id):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
    await conn.close()
    return row

async def get_top_users():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch('SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10')
    await conn.close()
    return rows
