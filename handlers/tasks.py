from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db, pool

router = Router()
ADMIN_ID = 1894004023

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message):
    try:
        tasks_list = await get_tasks()
        if not tasks_list:
            await message.answer("📭 <b>No challenges available.</b>", parse_mode="HTML")
            return

        builder = InlineKeyboardBuilder()
        for t in tasks_list:
            builder.row(types.InlineKeyboardButton(text=f"🔓 {t['title']} — {t['points']}pt", callback_data=f"view_{t['id']}"))
            if message.from_user.id == ADMIN_ID:
                builder.row(types.InlineKeyboardButton(text=f"🗑 Delete Task", callback_data=f"del_{t['id']}"))

        await message.answer("📋 <b>AVAILABLE CHALLENGES:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        await message.answer(f"⚠️ Error loading tasks: {e}")

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery, bot: Bot):
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    
    if not t:
        await callback.answer("Task not found!")
        return

    text = f"🚩 <b>{t['title']}</b>\nPoints: {t['points']}\n\nSubmit flag!"
    
    # Rasm yoki fayl borligini tekshirish
    if t.get('file_id'):
        try:
            await bot.send_document(chat_id=callback.message.chat.id, document=t['file_id'], caption=text, parse_mode="HTML")
        except:
            await bot.send_photo(chat_id=callback.message.chat.id, photo=t['file_id'], caption=text, parse_mode="HTML")
    else:
        await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    task_id = int(callback.data.split("_")[1])
    await delete_task_db(task_id)
    await callback.message.delete()
    await callback.answer("✅ Task deleted!")

@router.message(F.text.startswith("SPARK{"))
async def check_flag(message: types.Message):
    async with pool.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE flag = $1", message.text.strip())
        if not task:
            await message.answer("❌ <b>Wrong flag!</b>", parse_mode="HTML")
            return
        
        solved = await conn.fetchrow("SELECT * FROM solves WHERE user_id = $1 AND task_id = $2", message.from_user.id, task['id'])
        if solved:
            await message.answer("⚠️ You already solved this!")
            return

        await conn.execute("INSERT INTO solves (user_id, task_id, points) VALUES ($1, $2, $3)", message.from_user.id, task['id'], task['points'])
        await conn.execute("UPDATE users SET points = points + $1, solved_count = solved_count + 1 WHERE user_id = $2", task['points'], message.from_user.id)
        await message.answer(f"🎉 <b>Correct!</b> +{task['points']} pts", parse_mode="HTML")
