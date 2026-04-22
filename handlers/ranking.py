from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import get_top_users, get_user
from utils import generate_ranking_image
from locales import get_text

router = Router()

RANKING_BTNS = ["🏆 Ranking", "🏆 Рейтинг", "🏆 Reyting"]

@router.message(StateFilter("*"), F.text.in_(RANKING_BTNS))
@router.message(StateFilter("*"), Command("ranking"))
async def show_ranking(message: types.Message, state: FSMContext):
    await state.clear()
    try:
        user = await get_user(message.from_user.id)
        lang = user.get('language', 'en') if user else 'en'
        
        top = await get_top_users()
        
        if not top:
            await message.answer(get_text(lang, "ranking_empty"), parse_mode="HTML")
            return

        # User IDs for solve history
        uids = [u['user_id'] for u in top]
        from database import get_solve_history
        solves = await get_solve_history(uids)

        # Jadval rasmlarini yaratish
        from utils import generate_scoreboard_chart
        bar_chart_bytes = generate_ranking_image(top)
        line_chart_bytes = generate_scoreboard_chart(top, solves)
        
        text = get_text(lang, "ranking_title")
        
        medals = ["🥇", "🥈", "🥉"]
        for i, u in enumerate(top):
            rank = medals[i] if i < 3 else f"  <b>{i + 1}.</b>"
            nickname = u['nickname']
            if nickname:
                nickname = nickname.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            else:
                nickname = "Unknown"
            points = u['points']
            text += f"{rank}  <b>{nickname}</b>  •  {points} pts\n"
            
        text += get_text(lang, "ranking_footer")
        
        # Media group yuborish
        media = []
        if line_chart_bytes:
            media.append(types.InputMediaPhoto(media=types.BufferedInputFile(line_chart_bytes, filename="line.png")))
        if bar_chart_bytes:
            media.append(types.InputMediaPhoto(media=types.BufferedInputFile(bar_chart_bytes, filename="bar.png"), caption=text, parse_mode="HTML"))
        
        if media:
            await message.answer_media_group(media=media)
        else:
            await message.answer(text, parse_mode="HTML")
    except Exception as e:
        print(f"Error in ranking: {e}")
        await message.answer("⚠️ Error loading scoreboard. Please try again later.")
