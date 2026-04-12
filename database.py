import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        await conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY, nickname TEXT, points INTEGER DEFAULT 0, solved_count INTEGER DEFAULT 0
        )''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY, title TEXT, description TEXT, points INTEGER, flag TEXT
        )''')
        await conn.execute('''CREATE TABLE IF NOT EXISTS solves (
            id SERIAL PRIMARY KEY, user_id BIGINT, task_id INTEGER, points INTEGER, solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

async def add_user(user_id, nickname):
    async with pool.acquire() as conn:
        await conn.execute("INSERT INTO users (user_id, nickname) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET nickname = $2", user_id, nickname)

async def get_user(user_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)

async def get_tasks():
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT * FROM tasks ORDER BY points ASC')

async def add_new_task(title, description, points, flag):
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO tasks (title, description, points, flag) VALUES ($1, $2, $3, $4)', title, description, points, flag)

async def delete_task_db(task_title):
    async with pool.acquire() as conn:
        await conn.execute("DELETE FROM tasks WHERE title = $1", task_title)

async def clear_all_tasks():
    async with pool.acquire() as conn:
        await conn.execute("TRUNCATE TABLE tasks, solves RESTART IDENTITY")
