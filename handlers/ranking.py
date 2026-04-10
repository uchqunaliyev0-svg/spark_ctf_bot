import matplotlib.pyplot as plt
import io
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from database import get_top_users, pool  # pool bazaga ulanish uchun kerak

router = Router()

@router.message(F.text == "🏆 Ranking")
@router.message(Command("ranking"))
async def show_ranking(message: types.Message):
    # 1. Matnli reytingni olish
    users = await get_top_users()
    if not users:
        await message.answer("Leaderboard is empty.")
        return

    # 2. Grafik uchun bazadan tarixni olish (solves jadvalidan)
    async with pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.nickname, s.points, s.solved_at
            FROM solves s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.user_id IN (
                SELECT user_id FROM users ORDER BY points DESC LIMIT 10
            )
            ORDER BY s.solved_at ASC;
        """)

    # 3. Matnli qismni tayyorlash
    ranking_text = "🏆 **Top 10 Hackers**\n\n"
    for i, user in enumerate(users, 1):
        ranking_text += f"{i}. {user['nickname']} — {user['points']} pts\n"

    if not rows:
        # Agar hali hech kim task bajarmagan bo'lsa, faqat matnni o'zini yuboramiz
        await message.answer(ranking_text, parse_mode="Markdown")
        return

    # 4. GRAFIK CHIZISH (Matplotlib)
    plt.style.use('dark_background') # Qora fon
    fig, ax = plt.subplots(figsize=(10, 6))
    
    user_data = {}
    for row in rows:
        nick = row['nickname']
        if nick not in user_data:
            user_data[nick] = {'t': [], 'p': []}
        
        # Ballarni qo'shib borish (kumulyativ)
        last_p = user_data[nick]['p'][-1] if user_data[nick]['p'] else 0
        user_data[nick]['t'].append(row['solved_at'])
        user_data[nick]['p'].append(last_p + row['points'])

    # Har bir foydalanuvchi uchun alohida "zina" chizig'i
    for nick, data in user_data.items():
        ax.step(data['t'], data['p'], label=nick, where='post', linewidth=2, marker='o', markersize=4)

    ax.set_title("SparkCTF: Top 10 Growth", color='#00ff00', fontsize=14)
    ax.set_ylabel("Points")
    ax.grid(True, linestyle='--', alpha=0.2)
    plt.xticks(rotation=30)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
    plt.tight_layout()

    # 5. Rasmni xotiraga saqlash va yuborish
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    
    photo = BufferedInputFile(buf.read(), filename="ranking.png")
    
    # Rasm + Matn birga ketadi
    await message.answer_photo(
        photo=photo, 
        caption=ranking_text, 
        parse_mode="Markdown"
    )
    plt.close() # Xotirani tozalash
