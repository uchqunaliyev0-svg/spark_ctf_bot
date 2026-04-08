from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from database import get_user, add_user
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
        # Indeks bo'yicha olish: user[3] bu language, user[1] bu nickname
        lang = user[3] if len(user) > 3 else "uz"
        nick = user[1]
        
        welcome_msgs = {
            "uz": f"🔥 Qaytganingiz bilan, {nick}!",
            "ru": f"🔥 С возвращением, {nick}!",
            "en": f"🔥 Welcome back, {nick}!"
        }
        
        await message.answer(welcome_msgs.get(lang, welcome_msgs["uz"]), 
                             reply_markup=get_main_menu(lang))

@router.callback_query(F.data.startswith("lang_"))
async def set_lang(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split("_")[1]
    await state.update_data(language=lang)
    
    msgs = {
        "uz": "Ismingiz yoki Nickname kiriting:", 
        "ru": "Введите никнейм:", 
        "en": "Enter your nickname:"
    }
    await callback.message.answer(msgs[lang])
    await state.set_state(Register.nickname)
    await callback.answer()

@router.message(Register.nickname)
async def set_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    data = await state.get_data()
    lang = data['language']
    
    msgs = {
        "uz": "Davlatni kiriting (Masalan: 🇺🇿 O'zbekiston):", 
        "ru": "Введите страну (Например: 🇷🇺 Россия):", 
        "en": "Enter your country (e.g. 🇺🇸 USA):"
    }
    await message.answer(msgs[lang])
    await state.set_state(Register.country)

@router.message(Register.country)
async def set_country(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = message.from_user.id
    lang = data['language']
    nickname = data['nickname']
    country = message.text
    
    # Bazaga yozish
    await add_user(user_id, nickname, country, lang)
    await state.clear()
    
    final_msgs = {
        "uz": "Tayyor! ✅ Endi menyudan foydalanishingiz mumkin.", 
        "ru": "Готово! ✅ Теперь вы можете использовать меню.", 
        "en": "Done! ✅ Now you can use the menu."
    }
    await message.answer(final_msgs[lang], reply_markup=get_main_menu(lang))
