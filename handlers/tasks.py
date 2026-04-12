from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db, pool

router = Router()
ADMIN_ID = 1894004023

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message):
    tasks_list = await get_tasks()
    if not tasks_list:
        await message.answer("📭 <b>No challenges available.</b>", parse_mode="HTML")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        # Foydalanuvchi uchun tugma
        builder.row(types.InlineKeyboardButton(text=f"🔓 {t['title']} — {t['points']}pt", callback_data=f"view_{t['id']}"))
        
        # FAQAT SEN UCHUN (ADMIN): O'chirish tugmasi
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(text=f"🗑 Delete Task", callback_data=f"del_{t['id']}"))

    await message.answer("📋 <b>CHALLENGES:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    if t:
        text = f"🚩 <b>{t['title']}</b>\nPoints: {t['points']}\n\nSubmit flag in chat!"
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
async def flag_checker(message: types.Message):
    async with pool.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE flag = $1", message.text.strip())
        if not task:
            await message.answer("❌ <b>Wrong flag!</b>", parse_mode="HTML")
            return
        
        # Ball berish logikasi bu yerda...
        await message.answer(f"🎉 <b>Correct!</b> +{task['points']} pts", parse_mode="HTML")
