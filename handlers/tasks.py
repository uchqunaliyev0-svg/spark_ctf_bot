from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import get_tasks, delete_task_db, pool, get_user
from locales import get_text
from config import ADMIN_ID

router = Router()

CHALLENGES_BTNS = ["🎯 Challenges", "🎯 Задачи", "🎯 Vazifalar"]

@router.message(StateFilter("*"), F.text.in_(CHALLENGES_BTNS))
@router.message(StateFilter("*"), Command("tasks"))
async def show_categories(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    from database import get_categories
    categories = await get_categories()
    
    if not categories:
        await message.answer(get_text(lang, "no_tasks"), parse_mode="HTML")
        return

    builder = InlineKeyboardBuilder()
    for cat in categories:
        builder.button(text=f"📁 {cat['category']}", callback_data=f"category_{cat['category']}")
    builder.adjust(2)

    await message.answer(f"📂 <b>{get_text(lang, 'select_category')}</b>", reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data.startswith("category_"))
async def select_category(callback: types.CallbackQuery, bot: Bot):
    await callback.answer()
    category = callback.data.split("_")[1]
    
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    from database import get_tasks_by_category
    tasks_list = await get_tasks_by_category(category)
    
    if not tasks_list:
        await callback.message.answer(get_text(lang, "no_tasks"), parse_mode="HTML")
        return

    builder = InlineKeyboardBuilder()
    for t in tasks_list:
        builder.row(types.InlineKeyboardButton(text=f"{t['title']} — {t['points']}pt", callback_data=f"view_{t['id']}"))
        if callback.from_user.id == ADMIN_ID:
            builder.row(types.InlineKeyboardButton(text=f"Delete Task", callback_data=f"del_{t['id']}"))
    
    builder.row(types.InlineKeyboardButton(text="⬅️ Back", callback_data="back_to_categories"))

    await callback.message.edit_text(f"📂 Category: <b>{category}</b>\n\n<b>{get_text(lang, 'select_task')}</b>", reply_markup=builder.as_markup(), parse_mode="HTML")

@router.callback_query(F.data == "back_to_categories")
async def back_to_categories(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await show_categories(callback.message, state)

@router.callback_query(F.data.startswith("view_"))
async def view_task(callback: types.CallbackQuery, bot: Bot):
    await callback.answer() # Answer immediately to stop the loading spinner
    user = await get_user(callback.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    task_id = int(callback.data.split("_")[1])
    async with pool.acquire() as conn:
        t = await conn.fetchrow("SELECT * FROM tasks WHERE id = $1", task_id)
    
    if not t:
        await callback.message.answer("Task not found!")
        return

    text = get_text(lang, "task_format").format(t['title'], t['points'])
    
    # Check if there is a file attached
    if t.get('file_id'):
        try:
            await bot.send_document(chat_id=callback.message.chat.id, document=t['file_id'], caption=text, parse_mode="HTML")
        except Exception:
            try:
                await bot.send_photo(chat_id=callback.message.chat.id, photo=t['file_id'], caption=text, parse_mode="HTML")
            except Exception as e:
                await callback.message.answer(f"{text}\n\n[Attached file could not be sent: {e}]", parse_mode="HTML")
    else:
        await callback.message.answer(text, parse_mode="HTML")

@router.callback_query(F.data.startswith("del_"))
async def delete_handler(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID: return
    task_id = int(callback.data.split("_")[1])
    await delete_task_db(task_id)
    await callback.message.delete()
    await callback.answer("✅ Task deleted!")

@router.message(StateFilter("*"), F.text.startswith("SPARK{"))
async def check_flag(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user(message.from_user.id)
    lang = user.get('language', 'en') if user else 'en'
    
    async with pool.acquire() as conn:
        task = await conn.fetchrow("SELECT * FROM tasks WHERE flag = $1", message.text.strip())
        if not task:
            await message.answer(get_text(lang, "wrong_flag"), parse_mode="HTML")
            return
        
        solved = await conn.fetchrow("SELECT * FROM solves WHERE user_id = $1 AND task_id = $2", message.from_user.id, task['id'])
        if solved:
            await message.answer(get_text(lang, "already_solved"))
            return

        await conn.execute("INSERT INTO solves (user_id, task_id, points) VALUES ($1, $2, $3)", message.from_user.id, task['id'], task['points'])
        await conn.execute("UPDATE users SET points = points + $1, solved_count = solved_count + 1 WHERE user_id = $2", task['points'], message.from_user.id)
        await message.answer(get_text(lang, "correct_flag").format(task['points']), parse_mode="HTML")
