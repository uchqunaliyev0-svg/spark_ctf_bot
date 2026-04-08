from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user, count_users
from keyboards.main_menu import get_lang_keyboard, get_main_menu

router = Router()

class Register(StatesGroup):
    language = State()
    nickname = State()
    country = State()

@router.message(Command("start"))
async def start_cmd(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if not user:
        await message.answer("🌐 Tilni tanlang / Выберите язык / Choose language:", 
                             reply_markup=get_lang_keyboard())
        await state.set_state(Register.language)
    else:
        # Ro'yxatdan o'tgan bo'lsa, o'z tilida menyu chiqarish
        lang = user.get('language', 'uz') # Bazaga language ustuni qo'shish kerak
        await message.answer(f"🔥 Welcome back, {user['full_name']}!", 
                             reply_markup=get_main_menu(lang))

@router.callback_query(Register.language)
async def set_lang(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)
    
    msgs = {"uz": "Ismingiz yoki Nickname kiriting:", "ru": "Введите имя или никнейм:", "en": "Enter your nickname:"}
    await callback.message.answer(msgs[lang])
    await state.set_state(Register.nickname)
    await callback.answer()

@router.message(Register.nickname)
async def set_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    data = await state.get_data()
    lang = data['language']
    
    msgs = {"uz": "Davlatni kiriting 🌍:", "ru": "Введите страну 🌍:", "en": "Enter your country 🌍:"}
    await message.answer(msgs[lang])
    await state.set_state(Register.country)

@router.message(Register.country)
async def set_country(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    
    # Bazaga hamma ma'lumotni yozish
    # database.py dagi add_user funksiyasini shunga moslab yangilash kerak
    await add_user(user_id, data['nickname'], message.text, data['language'])
    await state.clear()
    
    msgs = {"uz": "Tayyor! ✅", "ru": "Готово! ✅", "en": "Done! ✅"}
    await message.answer(msgs[data['language']], reply_markup=get_main_menu(data['language']))
