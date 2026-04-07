import asyncpg
import os

# Railway variables-dan DATABASE_URL ni oladi
DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    # PostgreSQL-ga ulanish
    conn = await asyncpg.connect(DATABASE_URL)
    # Foydalanuvchilar jadvalini yaratish
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            full_name TEXT,
            points INTEGER DEFAULT 0,
            tasks_solved INTEGER DEFAULT 0
        )
    ''')
    await conn.close()

async def add_user(user_id, full_name):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO users (user_id, full_name) 
        VALUES ($1, $2) 
        ON CONFLICT (user_id) DO NOTHING
    ''', user_id, full_name)
    await conn.close()
