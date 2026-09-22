import aiosqlite
import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "spark_ctf.db")
db: aiosqlite.Connection = None


async def init_db():
    global db
    db = await aiosqlite.connect(
        DB_PATH,
        detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    )
    db.row_factory = aiosqlite.Row

    await db.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        nickname TEXT,
        points INTEGER DEFAULT 0,
        solved_count INTEGER DEFAULT 0,
        language TEXT DEFAULT 'en'
    )''')
    await db.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        points INTEGER,
        flag TEXT,
        file_id TEXT DEFAULT NULL,
        hint TEXT DEFAULT NULL,
        category TEXT DEFAULT 'General'
    )''')
    await db.execute('''CREATE TABLE IF NOT EXISTS solves (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_id INTEGER,
        points INTEGER,
        solved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    await db.commit()


async def add_user(user_id, nickname, lang='en'):
    await db.execute(
        '''INSERT INTO users (user_id, nickname, language) VALUES (?, ?, ?)
           ON CONFLICT (user_id) DO UPDATE SET nickname = excluded.nickname''',
        (user_id, nickname, lang)
    )
    await db.commit()


async def get_user(user_id):
    async with db.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)) as cur:
        return await cur.fetchone()


async def update_user_nickname(user_id, new_nickname):
    await db.execute("UPDATE users SET nickname = ? WHERE user_id = ?", (new_nickname, user_id))
    await db.commit()


async def update_user_language(user_id, lang):
    await db.execute("UPDATE users SET language = ? WHERE user_id = ?", (lang, user_id))
    await db.commit()


async def get_all_users():
    async with db.execute('SELECT user_id FROM users') as cur:
        return await cur.fetchall()


async def get_tasks():
    async with db.execute('SELECT * FROM tasks ORDER BY id ASC') as cur:
        return await cur.fetchall()


async def get_categories():
    async with db.execute('SELECT DISTINCT category FROM tasks ORDER BY category ASC') as cur:
        return await cur.fetchall()


async def get_tasks_by_category(category):
    async with db.execute('SELECT * FROM tasks WHERE category = ? ORDER BY points ASC', (category,)) as cur:
        return await cur.fetchall()


async def get_top_users():
    async with db.execute(
        "SELECT user_id, nickname, points FROM users ORDER BY points DESC LIMIT 10"
    ) as cur:
        return await cur.fetchall()


async def get_solve_history(user_ids):
    if not user_ids:
        return []
    placeholders = ','.join('?' * len(user_ids))
    async with db.execute(
        f"SELECT user_id, points, solved_at FROM solves "
        f"WHERE user_id IN ({placeholders}) ORDER BY solved_at ASC",
        list(user_ids)
    ) as cur:
        return await cur.fetchall()


async def add_new_task(title, points, flag, category='General', file_id=None, hint=None):
    await db.execute(
        'INSERT INTO tasks (title, points, flag, category, file_id, hint) VALUES (?, ?, ?, ?, ?, ?)',
        (title, points, flag, category, file_id, hint)
    )
    await db.commit()


async def delete_task_db(task_id):
    await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    await db.commit()


async def clear_all_tasks():
    await db.execute("DELETE FROM tasks")
    await db.execute("DELETE FROM solves")
    await db.execute("DELETE FROM sqlite_sequence WHERE name IN ('tasks', 'solves')")
    await db.commit()


async def get_task_by_id(task_id):
    async with db.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)) as cur:
        return await cur.fetchone()


async def get_task_by_flag(flag):
    async with db.execute("SELECT * FROM tasks WHERE flag = ?", (flag,)) as cur:
        return await cur.fetchone()


async def is_task_solved(user_id, task_id):
    async with db.execute(
        "SELECT 1 FROM solves WHERE user_id = ? AND task_id = ?", (user_id, task_id)
    ) as cur:
        return await cur.fetchone() is not None


async def submit_solve(user_id, task_id, points):
    await db.execute(
        "INSERT INTO solves (user_id, task_id, points) VALUES (?, ?, ?)",
        (user_id, task_id, points)
    )
    await db.execute(
        "UPDATE users SET points = points + ?, solved_count = solved_count + 1 WHERE user_id = ?",
        (points, user_id)
    )
    await db.commit()
