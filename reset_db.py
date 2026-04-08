import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def reset():
    try:
        conn = await asyncpg.connect(os.getenv('DATABASE_URL'))
        await conn.execute('DROP TABLE IF EXISTS users CASCADE')
        print("✅ DATABASE DROPPED!")
        await conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(reset())
