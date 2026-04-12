from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

@router.message(F.text == "👤 Profile", state="*")
async def show_profile(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    
    if not user:
        await message.answer("❌ Profile not found. Press /start.")
        return

    text = (
        f"👤 **SPARK CTF PROFILE**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏷 **Nick:** {user['nickname']}\n"
        f"💰 **Points:** {user['points']} pts\n"
        f"🚩 **Solved:** {user['solved_count']} tasks\n"
        f"🆔 **ID:** `{user['user_id']}`"
    )
    await message.answer(text, parse_mode="Markdown")
