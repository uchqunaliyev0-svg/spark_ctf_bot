from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db, pool

router = Router()
ADMIN_ID = 5472714251

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message):
    tasks_list = await get_tasks()
    if not tasks_list:
        await message.answer("📭 <b>No challenges active.</b>", parse_mode="HTML")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        builder.row(types.InlineKeyboardButton(text=f"🔓 {t['title']} — {t['points']}pt", callback_data=f"view_{t['id']}"))
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(text=f"🗑 Delete Task", callback_data=f"del_{t['id']}"))

    await message.answer("📋 <b>CHALLENGES:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    if t:
        text = f"🚩 <b>TASK: {t['title']}</b>\nPoints: {t['points']}\n\n<i>Submit flag in chat to solve!</i>"
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
    # Flag tekshirish mantiqi (Boya yozganimizdek)
    async with pool.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE flag = $1", message.text.strip())
        if not task:
            await message.answer("❌ Wrong flag!")
            return
        # Ball berish qismi...
        await message.answer(f"🎉 Correct! +{task['points']} pts")
