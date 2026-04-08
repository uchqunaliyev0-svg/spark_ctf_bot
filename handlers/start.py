from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import add_user, get_user
from keyboards.main_menu import get_main_menu # menyu tugmalaring nomi boshqacha bo'lsa to'g'irlab qo'y

router = Router()

# Ro'yxatdan o'tish holatlari
class RegState(StatesGroup):
    waiting_for_name = State()
    waiting_for_university = State()
    waiting_for_level = State()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(f"Xush kelibsiz, {user['full_name']}! Boshlashga tayyormisiz?", reply_markup=get_main_menu())
    else:
        await message.answer("Salom! Spark CTF botiga xush kelibsiz. \nRo'yxatdan o'tishni boshlaymiz. Ism-familiyangizni kiriting:")
        await state.set_state(RegState.waiting_for_name)

@router.message(RegState.waiting_for_name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Qayerda o'qiysiz yoki ishlaysiz? (Masalan: Cyber University)")
    await state.set_state(RegState.waiting_for_university)

@router.message(RegState.waiting_for_university)
async def get_uni(message: types.Message, state: FSMContext):
    await state.update_data(uni=message.text)
    # Darajani tanlash uchun oddiy tugmalar
    kb = [
        [types.KeyboardButton(text="Beginner"), types.KeyboardButton(text="Intermediate")],
        [types.KeyboardButton(text="Pro")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Hacking darajangizni tanlang:", reply_markup=keyboard)
    await state.set_state(RegState.waiting_for_level)

@router.message(RegState.waiting_for_level)
async def get_level(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await add_user(message.from_user.id, data['name'], data['uni'], message.text)
    await state.clear()
    await message.answer("Tabriklaymiz! Ro'yxatdan o'tdingiz. \nEndi CTF topshiriqlarini boshlashingiz mumkin.", reply_markup=get_main_menu())









