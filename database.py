import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        # Jadvallarni yaratish
        await conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY, nickname TEXT, points INTEGER DEFAULT 0, solved_count INTEGER DEFAULT 0, language TEXT DEFAULT 'en'
        )''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY, title TEXT, points INTEGER, flag TEXT, 
            file_id TEXT DEFAULT NULL, hint TEXT DEFAULT NULL
        )''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS solves (
            id SERIAL PRIMARY KEY, user_id BIGINT, task_id INTEGER, points INTEGER, solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # --- MAJBURIY MIGRATSIYA ---
        # Agar jadval bor bo'lsa-yu, ustunlar bo'lmasa, ularni qo'shamiz
        columns_tasks = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'tasks'")
        existing_columns_tasks = [col['column_name'] for col in columns_tasks]
        
        if 'file_id' not in existing_columns_tasks:
            await conn.execute("ALTER TABLE tasks ADD COLUMN file_id TEXT DEFAULT NULL")
        if 'hint' not in existing_columns_tasks:
            await conn.execute("ALTER TABLE tasks ADD COLUMN hint TEXT DEFAULT NULL")
            
        columns_users = await conn.fetch("SELECT column_name FROM information_schema.columns WHERE table_name = 'users'")
        existing_columns_users = [col['column_name'] for col in columns_users]
        if 'language' not in existing_columns_users:
            await conn.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")

async def add_user(user_id, nickname, lang='en'):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO users (user_id, nickname, language) VALUES ($1, $2, $3) ON CONFLICT (user_id) DO UPDATE SET nickname = $2", user_id, nickname, lang)

async def get_user(user_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)

async def update_user_nickname(user_id, new_nickname):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE users SET nickname = $1 WHERE user_id = $2", new_nickname, user_id)

async def update_user_language(user_id, lang):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE users SET language = $1 WHERE user_id = $2", lang, user_id)

async def get_all_users():
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT user_id FROM users')

async def get_tasks():
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT * FROM tasks ORDER BY id ASC')

async def get_top_users():
    async with pool.acquire() as conn:
        return await conn.fetch("SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10")

async def add_new_task(title, points, flag, file_id=None, hint=None):
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO tasks (title, points, flag, file_id, hint) VALUES ($1, $2, $3, $4, $5)', title, points, flag, file_id, hint)

async def delete_task_db(task_id):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM tasks WHERE id = $1", task_id)

async def clear_all_tasks():
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE tasks, solves RESTART IDENTITY")
