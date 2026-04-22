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
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    top = await get_top_users()
    
    if not top:
        await message.answer(get_text(lang, "ranking_empty"), parse_mode="HTML")
        return

    # Jadval rasmini yaratish
    image_bytes = generate_ranking_image(top)
    
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
    
    if image_bytes:
        photo = types.BufferedInputFile(image_bytes, filename="ranking.png")
        await message.answer_photo(photo=photo, caption=text, parse_mode="HTML")
    else:
        await message.answer(text, parse_mode="HTML")
