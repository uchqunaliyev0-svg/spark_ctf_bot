import asyncpg, os
DATABASE_URL = os.getenv("DATABASE_URL")
async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    # MANA SHU QATOR HAMMASINI TOZALAYDI:
    await conn.execute('DROP TABLE IF EXISTS users CASCADE')
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id BIGINT PRIMARY KEY, 
            nickname TEXT, 
            points INTEGER DEFAULT 0, 
            solved_count INTEGER DEFAULT 0
        )''')
    await conn.close()
