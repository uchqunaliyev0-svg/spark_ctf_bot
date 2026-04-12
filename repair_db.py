import asyncio
import os
import asyncpg

async def repair():
    conn = await asyncpg.connect(os.getenv("DATABASE_URL"))
    # Agar file_id ustuni bo'lmasa, uni qo'shamiz
    await conn.execute("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS file_id TEXT DEFAULT NULL")
    await conn.execute("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS hint TEXT DEFAULT NULL")
    await conn.close()
    print("✅ Database columns added successfully!")

if __name__ == "__main__":
    asyncio.run(repair())
