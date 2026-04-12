from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task, clear_all_tasks, get_all_users
import asyncio

router = Router()
ADMIN_ID = 1894004023

class AdminStates(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_task_points = State()
    waiting_for_task_flag = State()
    waiting_for_broadcast_msg = State()

@router.message(Command("addtask"))
async def start_add(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("🛠 <b>NEW TASK:</b> Enter title:", parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_task_title)

# ... (Vazifa qo'shish logikasi tepada o'zgarmaydi, faqat state nomlari AdminStates bo'ldi)
@router.message(AdminStates.waiting_for_task_title)
async def proc_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("💰 Points:")
    await state.set_state(AdminStates.waiting_for_task_points)

@router.message(AdminStates.waiting_for_task_points)
async def proc_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit(): return
    await state.update_data(points=int(message.text))
    await message.answer("🚩 Flag (SPARK{...}):")
    await state.set_state(AdminStates.waiting_for_task_flag)

@router.message(AdminStates.waiting_for_task_flag)
async def proc_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_new_task(data['title'], data['points'], message.text)
    await state.clear()
    await message.answer("✅ Task Added!")

# --- BROADCASTING SECTION ---
@router.message(Command("broadcast"))
async def start_broadcast(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID: return
    await message.answer("📢 <b>BROADCAST:</b> Send the message for ALL users:", parse_mode="HTML")
    await state.set_state(AdminStates.waiting_for_broadcast_msg)

@router.message(AdminStates.waiting_for_broadcast_msg)
async def send_broadcast(message: types.Message, state: FSMContext, bot: Bot):
    users = await get_all_users()
    count = 0
    await message.answer(f"⏳ Sending to {len(users)} users...")
    
    for user in users:
        try:
            # Matn, rasm yoki video — nima yuborsang ham hammasini ko'chirib yuboradi (Copy)
            await bot.copy_message(chat_id=user['user_id'], from_chat_id=message.chat.id, message_id=message.message_id)
            count += 1
            await asyncio.sleep(0.05) # Flood kontrol uchun kichik pauza
        except Exception:
            continue
            
    await state.clear()
    await message.answer(f"✅ Done! Successfully sent to {count} users.")
