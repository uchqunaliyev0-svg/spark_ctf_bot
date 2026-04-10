import matplotlib.pyplot as plt
import io
import database  # Modul sifatida import qilish NoneType xatosini oldini oladi
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import BufferedInputFile
from database import get_top_users

router = Router()

@router.message(F.text == "🏆 Ranking")
@router.message(Command("ranking"))
async def show_ranking(message: types.Message):
    # 1. Matnli TOP 10 ro'yxatni olish
    users = await get_top_users()
    if not users:
        await message.answer("📊 Leaderboard hozircha bo'sh.")
        return

    # 2. Grafik uchun tarixni olish (database.pool orqali)
    async with database.pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.nickname, s.points, s.solved_at
            FROM solves s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.user_id IN (
                SELECT user_id FROM users ORDER BY points DESC LIMIT 10
            )
            ORDER BY s.solved_at ASC;
        """)

    # 3. Matnli qismni shakllantirish
    text = "🏆 **Top 10 Hackers**\n\n"
    for i, user in enumerate(users, 1):
        text += f"{i}. {user['nickname']} — {user['points']} pts\n"

    # Agar tarix bo'sh bo'lsa (hali hech kim task yechmagan), faqat matnni yuboramiz
    if not rows:
        await message.answer(text, parse_mode="Markdown")
        return

    # 4. GRAFIK CHIZISH (Matplotlib)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    user_data = {}
    for row in rows:
        nick = row['nickname']
        if nick not in user_data:
            user_data[nick] = {'t': [], 'p': []}
        
        # Ballarni kumulyativ (o'sib boruvchi) hisoblash
        last_p = user_data[nick]['p'][-1] if user_data[nick]['p'] else 0
        user_data[nick]['t'].append(row['solved_at'])
        user_data[nick]['p'].append(last_p + row['points'])

    # Har bir user uchun "zina" chizig'ini chizish
    for nick, data in user_data.items():
        ax.step(data['t'], data['p'], label=nick, where='post', linewidth=2, marker='o', markersize=4)

    # Grafik bezaklari
    ax.set_title("SparkCTF: Hackers Growth", color='#00ff00', fontsize=14, pad=15)
    ax.set_ylabel("Points", color='gray')
    ax.grid(True, linestyle='--', alpha=0.1)
    plt.xticks(rotation=30, fontsize=8)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
    plt.tight_layout()

    # 5. Rasmni xotiraga saqlash va yuborish
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    
    photo = BufferedInputFile(buf.read(), filename="ranking.png")
    
    await message.answer_photo(
        photo=photo, 
        caption=text, 
        parse_mode="Markdown"
    )
    plt.close() # Xotirani bo'shatish
