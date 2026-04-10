import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    async with pool.acquire() as conn:
        # Users jadvali
        await conn.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY,
            nickname TEXT,
            points INTEGER DEFAULT 0,
            solved_count INTEGER DEFAULT 0
        )''')
        # Tasks jadvali
        await conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT,
            description TEXT,
            points INTEGER,
            flag TEXT
        )''')
        # Solves jadvali (Yechilgan tasklar tarixi)
        await conn.execute('''CREATE TABLE IF NOT EXISTS solves (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            task_id INTEGER,
            points INTEGER,
            solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

async def add_user(user_id, nickname):
    async with pool.acquire() as conn:
        await conn.execute('''INSERT INTO users (user_id, nickname)
                             VALUES ($1, $2)
                             ON CONFLICT (user_id) DO UPDATE SET nickname = $2''', user_id, nickname)

async def get_user(user_id):
    async with pool.acquire() as conn:
        return await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)

async def get_tasks():
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT * FROM tasks ORDER BY id DESC')

async def get_top_users():
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10')

async def check_flag_db(user_id, submitted_flag):
    async with pool.acquire() as conn:
        # Flagni tekshirish
        task = await conn.fetchrow('SELECT * FROM tasks WHERE flag = $1', submitted_flag)
        if task:
            # Avval yechganligini tekshirish
            solved = await conn.fetchrow('SELECT * FROM solves WHERE user_id = $1 AND task_id = $2', user_id, task['id'])
            if not solved:
                # 1. Solves jadvaliga yozish
                await conn.execute('INSERT INTO solves (user_id, task_id, points) VALUES ($1, $2, $3)',
                                   user_id, task['id'], task['points'])
                # 2. User balansini yangilash
                await conn.execute('UPDATE users SET points = points + $1, solved_count = solved_count + 1 WHERE user_id = $2',
                                   task['points'], user_id)
                return task['points']
        return None

async def get_total_users():
    async with pool.acquire() as conn:
        return await conn.fetchval('SELECT COUNT(*) FROM users')

async def add_new_task(title, description, points, flag):
    async with pool.acquire() as conn:
        await conn.execute(
            'INSERT INTO tasks (title, description, points, flag) VALUES ($1, $2, $3, $4)',
            title, description, points, flag
        )
