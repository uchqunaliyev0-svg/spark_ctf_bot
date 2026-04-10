from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_new_task

router = Router()

class AddTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_points = State()
    waiting_for_flag = State()

@router.message(F.text == "/addtask", state="*")
async def start_add(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("🛠 **Yangi Task Qo'shish**\n\nTask nomini kiriting:")
    await state.set_state(AddTask.waiting_for_title)

@router.message(AddTask.waiting_for_title)
async def process_title(message: types.Message, state: FSMContext):
    if message.text in ["👤 Profile", "🚩 Tasks", "🏆 Ranking"]: # Tugma bosilsa tunneldan chiqish
        await state.clear()
        return
    await state.update_data(title=message.text)
    await message.answer("💰 Necha ball beramiz? (Faqat raqam yozing):")
    await state.set_state(AddTask.waiting_for_points)

@router.message(AddTask.waiting_for_points)
async def process_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, faqat raqam kiriting!")
        return
    
    await state.update_data(points=int(message.text))
    await message.answer("🚩 Flagni kiriting (masalan: spark{...}):")
    await state.set_state(AddTask.waiting_for_flag)

@router.message(AddTask.waiting_for_flag)
async def process_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    # Bazaga qo'shish (database.py dagi add_new_task ishlatiladi)
    await add_new_task(data['title'], "Tavsif yo'q", data['points'], message.text)
    
    await state.clear()
    await message.answer("✅ Task muvaffaqiyatli qo'shildi!")
