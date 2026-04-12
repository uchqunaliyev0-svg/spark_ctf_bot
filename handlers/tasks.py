from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from database import get_tasks, pool

router = Router()
ADMIN_ID = 1894004023

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery, bot: Bot):
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    
    if t:
        text = f"🚩 <b>{t['title']}</b>\nPoints: {t['points']}\n\nSubmit flag!"
        
        # Agar fayl bo'lsa, uni yuboramiz
        if t['file_id']:
            try:
                await bot.send_document(chat_id=callback.message.chat.id, document=t['file_id'], caption=text, parse_mode="HTML")
            except:
                await bot.send_photo(chat_id=callback.message.chat.id, photo=t['file_id'], caption=text, parse_mode="HTML")
        else:
            await callback.message.answer(text, parse_mode="HTML")
            
    await callback.answer()
