from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db

router = Router()
ADMIN_ID = 5472714251 # Sening ID'ing

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 <b>No challenges available right now.</b>", parse_mode="HTML")
        return

    # Professional ko'rinish: Hamma tasklar bitta ro'yxatda tugma bo'lib chiqadi
    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        # Taskni ko'rish tugmasi
        builder.row(types.InlineKeyboardButton(
            text=f"🔓 {t['title']} — {t['points']}pt", 
            callback_data=f"view_{t['id']}")
        )
        
        # Admin bo'lsang, yoniga o'chirish tugmasini qo'shadi
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(
                text=f"🗑 Delete {t['title']}", 
                callback_data=f"del_{t['title']}")
            )

    await message.answer(
        "📋 <b>AVAILABLE CHALLENGES:</b>\nSelect a task below to see details.",
        reply_markup=builder.as_markup(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("view_"))
async def view_task_detail(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    from database import pool
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    
    if not t:
        await callback.answer("Task not found!")
        return

    text = (
        f"🚩 <b>TASK: {t['title']}</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💰 <b>Points:</b> {t['points']} pts\n\n"
        f"💡 <i>Submit the flag in the chat to solve!</i>"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("❌ No permission!", show_alert=True)
        return
        
    task_name = callback.data.split("_")[1]
    await delete_task_db(task_name)
    await callback.message.delete()
    await callback.answer(f"✅ {task_name} deleted!", show_alert=True)
