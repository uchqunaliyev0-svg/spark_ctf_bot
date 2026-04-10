from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.clear() # Har qanday tunnelni buzadi
    
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("❌ Profil topilmadi. /start bosing.")
        return

    text = (
        f"👤 **SPARK CTF PROFILI**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏷 **Nick:** {user['nickname']}\n"
        f"💰 **Ballar:** {user['points']} pt\n"
        f"🚩 **Yechilgan:** {user['solved_count']} ta\n"
        f"🆔 **ID:** `{user['user_id']}`"
    )
    await message.answer(text, parse_mode="Markdown")
