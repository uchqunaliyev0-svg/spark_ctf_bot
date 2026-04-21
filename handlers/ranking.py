from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from database import get_top_users
from utils import generate_ranking_image

router = Router()

@router.message(StateFilter("*"), F.text == "🏆 Ranking")
@router.message(StateFilter("*"), Command("ranking"))
async def show_ranking(message: types.Message, state: FSMContext):
    await state.clear()
    top = await get_top_users()
    
    if not top:
        await message.answer("🏆 <b>Global Leaderboard</b>\n\n<i>No one is on the leaderboard yet...</i>", parse_mode="HTML")
        return

    # Jadval rasmini yaratish
    image_bytes = generate_ranking_image(top)
    
    text = "🏆 <b>Global Leaderboard</b>\n"
    text += "━━━━━━━━━━━━━━━━━━\n\n"
    
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(top):
        rank = medals[i] if i < 3 else f"  <b>{i + 1}.</b>"
        nickname = user['nickname']
        if nickname:
            nickname = nickname.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        else:
            nickname = "Unknown"
        points = user['points']
        text += f"{rank}  <b>{nickname}</b>  •  {points} pts\n"
        
    text += "\n━━━━━━━━━━━━━━━━━━\n"
    text += "🎯 <i>Keep solving challenges to climb the ranks!</i>"
    
    if image_bytes:
        photo = types.BufferedInputFile(image_bytes, filename="ranking.png")
        await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")
