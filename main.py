import os
import asyncio
import matplotlib
matplotlib.use('Agg')  # Railway serverida grafik chizish uchun shart!
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.session.aiohttp import AiohttpSession

# --- 1. SOZLAMALAR ---
# Yangi SparkCTF tokeningni mana shu yerga qo'ydim:
TOKEN = "8725722196:AAFJ7-ADisGy_n8hPQph3yVhsGMCk9pSXBo"

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher()

class ProfileEdit(StatesGroup):
    waiting_for_name = State()

# --- 2. SCOREBOARD FUNKSIYASI ---
def create_scoreboard_graph():
    # Bu ma'lumotlarni kelajakda bazadan SELECT qilib olasan
    users = ["lowkeyciso", "yaasosed", "NothingsNwe", "alimovichx", "ubbyt"]
    scores = [2266, 1552, 1060, 1047, 790]
    
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    colors = ['#00ff00', '#00cc00', '#009900', '#006600', '#003300']
    plt.bar(users, scores, color=colors)
    plt.title("SparkCTF Global Scoreboard", color='#00ff00', fontsize=18)
    plt.ylabel("Points", color='white')
    plt.grid(axis='y', linestyle='--', alpha=0.2)
    
    graph_path = "spark_scoreboard.png"
    plt.savefig(graph_path)
    plt.close()
    return graph_path

# --- 3. BUYRUQLAR ---

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"⚡️ **SparkCTF Platformasiga xush kelibsiz!**\n\n"
        "Tizim tayyor. Quyidagi buyruqlardan foydalaning:\n"
        "📊 /scoreboard - Global reyting\n"
        "👤 /profile - Shaxsiy profilingiz",
        parse_mode="Markdown"
    )

@dp.message(Command("profile"))
async def profile(message: Message):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Ismni tahrirlash ✏️", callback_data="edit_name"))
    
    await message.answer(
        f"👤 **SparkCTF Profilingiz:**\n\n"
        f"Nik: `{message.from_user.username or 'O\'rnatilmagan'}`\n"
        f"Ochko: 1250\n"
        f"Rank: #15",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

@dp.message(Command("scoreboard"))
async def send_scoreboard(message: Message):
    wait_msg = await message.answer("📊 Grafik tayyorlanmoqda...")
    try:
        graph = create_scoreboard_graph()
        await message.answer_photo(FSInputFile(graph), caption="🔥 **Top 5 Global Hackers**\nSparkCTF'da birinchi bo'ling!")
        if os.path.exists(graph):
            os.remove(graph)
    except Exception as e:
        await message.answer(f"❌ Xato: {e}")
    finally:
        await wait_msg.delete()

# --- 4. FSM (EDIT NICKNAME) ---

@dp.callback_query(F.data == "edit_name")
async def edit_name_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("⌨️ Yangi nikingizni yuboring:")
    await state.set_state(ProfileEdit.waiting_for_name)
    await callback.answer()

@dp.message(ProfileEdit.waiting_for_name)
async def process_new_name(message: Message, state: FSMContext):
    new_name = message.text
    # Kelajakda bazaga yuborish: db.update(message.from_user.id, new_name)
    await message.answer(f"✅ Profil yangilandi! Yangi nikingiz: **{new_name}**", parse_mode="Markdown")
    await state.clear()

# --- 5. ISHGA TUSHIRISH ---
async def main():
    print("⚡️ @SparkCTF_bot muvaffaqiyatli ishga tushdi...")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot to'xtatildi!")
