import matplotlib.pyplot as plt
import io
import database
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

    # 2. Grafik uchun tarixni olish (SQL so'rov to'g'irlandi)
    async with database.pool.acquire() as conn:
        rows = await conn.fetch("""
            SELECT u.nickname, s.points as solve_points, s.solved_at
            FROM solves s
            JOIN users u ON s.user_id = u.user_id
            WHERE s.user_id IN (
                SELECT user_id FROM users ORDER BY points DESC LIMIT 10
            )
            ORDER BY s.solved_at ASC;
        """)

    # 3. Matnli qism
    text = "🏆 **Top 10 Hackers**\n\n"
    for i, user in enumerate(users, 1):
        text += f"{i}. {user['nickname']} — {user['points']} pts\n"

    if not rows:
        await message.answer(text, parse_mode="Markdown")
        return

    # 4. GRAFIK CHIZISH
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    user_data = {}
    for row in rows:
        nick = row['nickname']
        if nick not in user_data:
            user_data[nick] = {'t': [], 'p': []}
        
        last_p = user_data[nick]['p'][-1] if user_data[nick]['p'] else 0
        user_data[nick]['t'].append(row['solved_at'])
        user_data[nick]['p'].append(last_p + row['solve_points']) # solve_points ishlatamiz

    for nick, data in user_data.items():
        ax.step(data['t'], data['p'], label=nick, where='post', linewidth=2, marker='o', markersize=4)

    ax.set_title("SparkCTF: Hackers Growth", color='#00ff00', fontsize=14, pad=15)
    ax.set_ylabel("Points", color='gray')
    ax.grid(True, linestyle='--', alpha=0.1)
    plt.xticks(rotation=30, fontsize=8)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=8)
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=120)
    buf.seek(0)
    
    photo = BufferedInputFile(buf.read(), filename="ranking.png")
    await message.answer_photo(photo=photo, caption=text, parse_mode="Markdown")
    plt.close()
