async def add_user(user_id, nickname, country, language):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO users (user_id, full_name, university, experience_level)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (user_id) DO UPDATE
        SET full_name = $2, university = $3, experience_level = $4
    ''', user_id, nickname, country, language) # University o'rniga country, lvl o'rniga lang ketyapti vaqtinchalik
    await conn.close()
