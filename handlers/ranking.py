from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import pool

router = Router()

@router.message(F.text == "🏆 Ranking", state="*")
async def show_ranking(message: types.Message, state: FSMContext):
    await state.clear()
    
    async with pool.acquire() as conn:
        users = await conn.fetch("SELECT nickname, points FROM users ORDER BY points DESC LIMIT 10")
    
    if not users:
        await message.answer("📊 Reyting hali shakllanmagan.")
        return

    text = "🏆 **TOP 10 XAKERLAR:**\n\n"
    for i, u in enumerate(users, 1):
        text += f"{i}. {u['nickname']} — {u['points']} pt\n"
    
    await message.answer(text, parse_mode="Markdown")
