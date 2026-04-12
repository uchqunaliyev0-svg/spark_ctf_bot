from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db, pool

router = Router()
ADMIN_ID = 5472714251

@router.message(F.text == "🚩 Tasks")
@router.message(Command("tasks"))
async def show_tasks(message: types.Message, state: FSMContext):
    await state.clear()
    tasks_list = await get_tasks()
    if not tasks_list:
        await message.answer("📭 <b>No challenges available.</b>", parse_mode="HTML")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        builder.row(types.InlineKeyboardButton(text=f"🔓 {t['title']} — {t['points']}pt", callback_data=f"view_{t['id']}"))
        if message.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(text=f"🗑 Delete {t['title']}", callback_data=f"del_{t['title']}"))

    await message.answer("📋 <b>AVAILABLE CHALLENGES:</b>", reply_markup=builder.as_markup(), parse_mode="HTML")

# --- FLAG CHECKER LOGIC ---
@router.message(F.text.startswith("SPARK{"))
async def check_flag(message: types.Message):
    input_flag = message.text.strip()
    
    async with pool.acquire() as conn:
        # Bazadan shu flagli taskni qidiramiz
        task = await conn.fetchrow("SELECT * FROM tasks WHERE flag = $1", input_flag)
        
        if not task:
            await message.answer("❌ <b>Wrong flag!</b> Keep searching...", parse_mode="HTML")
            return

        # Avval yechganmi yoki yo'qmi tekshiramiz
        solved = await conn.fetchrow("SELECT * FROM solves WHERE user_id = $1 AND task_id = $2", 
                                     message.from_user.id, task['id'])
        
        if solved:
            await message.answer("⚠️ You have already solved this challenge!", parse_mode="HTML")
            return

        # Ochko beramiz va bazani yangilaymiz
        await conn.execute("INSERT INTO solves (user_id, task_id, points) VALUES ($1, $2, $3)",
                           message.from_user.id, task['id'], task['points'])
        
        await conn.execute("UPDATE users SET points = points + $1, solved_count = solved_count + 1 WHERE user_id = $2",
                           task['points'], message.from_user.id)
        
        await message.answer(f"🎉 <b>Correct!</b>\nYou earned <b>{task['points']}</b> points!", parse_mode="HTML")

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    if t:
        await callback.message.answer(f"🚩 <b>TASK: {t['title']}</b>\nPoints: {t['points']}\n\nSubmit flag in chat!", parse_mode="HTML")
    await callback.answer()

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    task_name = callback.data.split("_")[1]
    await delete_task_db(task_name)
    await callback.message.delete()
    await callback.answer(f"✅ {task_name} deleted!")
