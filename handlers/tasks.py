from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db

router = Router()
ADMIN_ID = 5472714251 # ID'ingni tekshirib qo'y

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    
    if not tasks_list:
        await message.answer("📭 **No challenges available right now.**", parse_mode="Markdown")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        builder.row(types.InlineKeyboardButton(
            text=f"🔓 {t['title']} — {t['points']}pt", 
            callback_data=f"view_{t['id']}")
        )
    
    await message.answer("📋 **AVAILABLE CHALLENGES:**", reply_markup=builder.as_markup())

@router.callback_query(F.data.startswith("view_"))
async def view_task_detail(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    from database import pool
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    
    if not t:
        await callback.answer("Task not found!")
        return

    text = f"🚩 **TASK: {t['title']}**\n💰 **Points:** {t['points']} pts\n📝 **Desc:** {t['description']}"
    
    builder = InlineKeyboardBuilder()
    if callback.from_user.id == ADMIN_ID:
        builder.row(types.InlineKeyboardButton(text="🗑 Delete Task", callback_data=f"del_{t['title']}"))
    
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    await callback.answer()

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    task_name = callback.data.split("_")[1]
    await delete_task_db(task_name)
    await callback.message.delete()
    await callback.answer(f"✅ {task_name} deleted!", show_alert=True)
