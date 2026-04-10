from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    # Har qanday holatni (state) tozalaymiz
    await state.clear()
    
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Profil topilmadi. /start bosing.")
        return

    text = (
        f"👤 **SPARK CTF PROFILI**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏷 **Nick:** {user['nickname']}\n"
        f"💰 **Ballar:** {user.get('points', 0)} pt\n"
        f"🚩 **Yechilgan:** {user.get('solved_count', 0)} ta\n"
    )
    await message.answer(text, parse_mode="Markdown")
