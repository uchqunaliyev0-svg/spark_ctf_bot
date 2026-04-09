from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_total_users

router = Router()

# SENING HAQIQIY ID RAQAMING (BOTNING XO'JAYINI):
ADMIN_ID = 1894004023

# FSM: Task qo'shish bosqichlari
class AddTask(StatesGroup):
    title = State()
    points = State()
    description = State()
    flag = State()

# --- 1. STATISTIKA BUYRUG'I ---
@router.message(Command("stats"))
async def show_stats(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    total = await get_total_users()
    await message.answer(f"📊 **Spark CTF Statistika**\n\n👤 Jami foydalanuvchilar: {total}", parse_mode="Markdown")

# --- 2. GOD MODE: TASK QO'SHISH ---
@router.message(Command("addtask"))
async def start_add_task(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("🛠 **Yangi Task Qo'shish (God Mode)**\n\nTask nomini kiriting (masalan: `Web Zaiflik v1`):", parse_mode="Markdown")
    await state.set_state(AddTask.title)

@router.message(AddTask.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("🔹 Bu task uchun qancha ball beramiz? (Faqat raqam yozing, masalan: `150`):")
    await state.set_state(AddTask.points)

@router.message(AddTask.points)
async def process_points(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("⚠️ Iltimos, faqat raqam kiriting!")
        return
    await state.update_data(points=int(message.text))
    await message.answer("📝 Task ta'rifini yozing (nima qilish kerakligi):")
    await state.set_state(AddTask.description)

@router.message(AddTask.description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("🚩 Yashirin Flag'ni kiriting (masalan: `spark{admin_bypassed}`):")
    await state.set_state(AddTask.flag)

@router.message(AddTask.flag)
async def process_flag(message: types.Message, state: FSMContext):
    data = await state.get_data()
    title = data['title']
    points = data['points']
    description = data['description']
    flag = message.text

    # Bazaga yozish
    from database import add_new_task
    await add_new_task(title, description, points, flag)

    await message.answer(f"✅ **Task muvaffaqiyatli qo'shildi!**\n\n📌 Nomi: {title}\n💰 Ball: {points}\n🚩 Flag: `{flag}`", parse_mode="Markdown")
    await state.clear()
