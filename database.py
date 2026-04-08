import asyncpg, os
DATABASE_URL = os.getenv("DATABASE_URL")

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    # Users table
    await conn.execute('CREATE TABLE IF NOT EXISTS users (user_id BIGINT PRIMARY KEY, nickname TEXT, points INTEGER DEFAULT 0, solved_count INTEGER DEFAULT 0)')
    # Tasks table
    await conn.execute('CREATE TABLE IF NOT EXISTS tasks (id SERIAL PRIMARY KEY, name TEXT, description TEXT, flag TEXT, points INTEGER)')
    # Solves table (kim qaysi taskni yechganini saqlash uchun)
    await conn.execute('CREATE TABLE IF NOT EXISTS solves (user_id BIGINT, task_id INTEGER, PRIMARY KEY (user_id, task_id))')
    await conn.close()

async def add_user(user_id, nickname):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('INSERT INTO users (user_id, nickname) VALUES ($1, $2) ON CONFLICT (user_id) DO UPDATE SET nickname = $2', user_id, nickname)
    await conn.close()

async def get_user(user_id):
    conn = await asyncpg.connect(DATABASE_URL)
    row = await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id)
    await conn.close()
    return row

async def get_tasks():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch('SELECT * FROM tasks')
    await conn.close()
    return rows

async def check_flag_db(user_id, submitted_flag):
    conn = await asyncpg.connect(DATABASE_URL)
    # Flagni tekshirish
    task = await conn.fetchrow('SELECT * FROM tasks WHERE flag = $1', submitted_flag)
    if task:
        # User avval yechganmi?
        solved = await conn.fetchrow('SELECT * FROM solves WHERE user_id = $1 AND task_id = $2', user_id, task['id'])
        if not solved:
            # Solves-ga qo'shish
            await conn.execute('INSERT INTO solves (user_id, task_id) VALUES ($1, $2)', user_id, task['id'])
            # User ballarini oshirish
            await conn.execute('UPDATE users SET points = points + $1, solved_count = solved_count + 1 WHERE user_id = $2', task['points'], user_id)
            await conn.close()
            return task['points']
    await conn.close()
    return None

async def get_top_users():
    conn = await asyncpg.connect(DATABASE_URL)
    rows = await conn.fetch('SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10')
    await conn.close()
    return rows
