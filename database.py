import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            nickname TEXT,
            country TEXT,
            language TEXT,
            points INTEGER DEFAULT 0
        )
    ''')
    await conn.close()

async def add_user(user_id, nickname, country, language):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO users (user_id, nickname, country, language)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (user_id) DO UPDATE
        SET nickname = $2, country = $3, language = $4
    ''', user_id, nickname, country, language)
    await conn.close()

async def get_user(user_id):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
    await conn.close()
    return row

async def count_users():
    conn = await asyncpg.connect(DATABASE_URL)
    count = await conn.fetchval('SELECT COUNT(*) FROM users')
    await conn.close()
    return count
