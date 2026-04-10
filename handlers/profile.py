from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from database import get_user

router = Router()

# DIQQAT: state="*" qo'shdik. Bu user har qanday tunnelda (state) 
# bo'lganida ham Profil tugmasi ishlashini ta'minlaydi.
@router.message(F.text == "👤 Profile", state="*")
@router.message(Command("profile"), state="*")
async def show_profile(message: types.Message, state: FSMContext):
    # 1. MUHIM: Har qanday FSM holatini (masalan, task qo'shishni) tozalaymiz
    await state.clear()

    user_id = message.from_user.id
    user = await get_user(user_id)

    if not user:
        await message.answer("⚠️ Profil ma'lumotlari topilmadi. Iltimos, /start bosing.")
        return

    # 2. Ma'lumotlarni bazadan olish
    nickname = user['nickname']
    points = user.get('points', 0)
    solved = user.get('solved_count', 0)

    # 3. Profil darajasini aniqlash
    if points < 500:
        rank = "Newbie 🐣"
    elif points < 1500:
        rank = "Script Kiddie 💻"
    elif points < 3000:
        rank = "Pro Hacker ⚡️"
    else:
        rank = "Cyber Ghost 👻"

    # 4. Chiroyli matn tayyorlash
    text = (
        f"👤 **SPARK CTF PROFILI**\n"
        f"━━━━━━━━━━━━━━━\n"
        f"🏷 **Nickname:** {nickname}\n"
        f"🆔 **User ID:** `{user_id}`\n"
        f"🏆 **Daraja:** {rank}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 **Jami ball:** {points} pt\n"
        f"🚩 **Yechilgan tasklar:** {solved} ta\n\n"
        f"📈 *Reytingda ko'tarilish uchun ko'proq task yeching!*"
    )

    # Profilni yuborish
    await message.answer(text, parse_mode="Markdown")
