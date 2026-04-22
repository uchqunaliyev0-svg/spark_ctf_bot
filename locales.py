# locales.py

texts = {
    "en": {
        "welcome": "👋 <b>Welcome to Spark CTF!</b>\nYou are not registered yet. Please enter your <b>Hacker Nickname</b>:",
        "nickname_error": "⚠️ Nickname must be between 3 and 15 characters!",
        "lang_choose": "🌐 Please choose your language:",
        "registered": "✅ Registered successfully as <b>{}</b>!",
        "welcome_back": "Welcome back, <b>{}</b>!",
        
        "btn_challenges": "🎯 Challenges",
        "btn_profile": "👤 Profile",
        "btn_ranking": "🏆 Ranking",
        "btn_info": "ℹ️ Info",
        
        "no_tasks": "No challenges available at the moment.",
        "select_task": "Select a challenge:",
        "task_format": "<b>{}</b>\nPoints: {} pts\n\nFormat: <code>SPARK{{flag_here}}</code>",
        "send_flag": "Send the flag to solve this challenge.",
        "already_solved": "You have already solved this challenge! ✅",
        "wrong_flag": "❌ Incorrect flag! Try again.",
        "correct_flag": "🎉 Correct! You gained {} pts.",
        
        "profile_text": "👤 <b>PROFILE</b>\n\n<b>Nick:</b> {}\n<b>Points:</b> {} pts\n<b>Solved:</b> {}",
        "ranking_empty": "🏆 <b>Global Leaderboard</b>\n\n<i>No one is on the leaderboard yet...</i>",
        "ranking_title": "🏆 <b>Global Leaderboard</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        "ranking_footer": "\n━━━━━━━━━━━━━━━━━━\n🎯 <i>Keep solving challenges to climb the ranks!</i>",
        
        "info_text": "<b>SPARK CTF PLATFORM</b>\n\n<b>Flag Format:</b> <code>SPARK{flag_here}</code>\n<b>Edit Nickname:</b> /rename\n\n<b>Developer:</b> @uchqun_aliyev\n<b>Status:</b> Secure Connection",
        
        "rename_prompt": "📝 Enter your <b>new hacker nickname:</b>",
        "rename_success": "✅ Your nickname has been updated to: <b>{}</b>"
    },
    "ru": {
        "welcome": "👋 <b>Добро пожаловать в Spark CTF!</b>\nВы еще не зарегистрированы. Пожалуйста, введите ваш <b>Никнейм</b>:",
        "nickname_error": "⚠️ Никнейм должен содержать от 3 до 15 символов!",
        "lang_choose": "🌐 Пожалуйста, выберите язык:",
        "registered": "✅ Вы успешно зарегистрированы как <b>{}</b>!",
        "welcome_back": "С возвращением, <b>{}</b>!",
        
        "btn_challenges": "🎯 Задачи",
        "btn_profile": "👤 Профиль",
        "btn_ranking": "🏆 Рейтинг",
        "btn_info": "ℹ️ Инфо",
        
        "no_tasks": "На данный момент нет доступных задач.",
        "select_task": "Выберите задачу:",
        "task_format": "<b>{}</b>\nОчки: {} pts\n\nФормат: <code>SPARK{{flag_here}}</code>",
        "send_flag": "Отправьте флаг для решения этой задачи.",
        "already_solved": "Вы уже решили эту задачу! ✅",
        "wrong_flag": "❌ Неверный флаг! Попробуйте еще раз.",
        "correct_flag": "🎉 Правильно! Вы получили {} pts.",
        
        "profile_text": "👤 <b>ПРОФИЛЬ</b>\n\n<b>Ник:</b> {}\n<b>Очки:</b> {} pts\n<b>Решено:</b> {}",
        "ranking_empty": "🏆 <b>Глобальный Рейтинг</b>\n\n<i>В рейтинге пока никого нет...</i>",
        "ranking_title": "🏆 <b>Глобальный Рейтинг</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        "ranking_footer": "\n━━━━━━━━━━━━━━━━━━\n🎯 <i>Решайте задачи, чтобы подняться в рейтинге!</i>",
        
        "info_text": "<b>SPARK CTF ПЛАТФОРМА</b>\n\n<b>Формат флага:</b> <code>SPARK{flag_here}</code>\n<b>Изменить ник:</b> /rename\n\n<b>Разработчик:</b> @uchqun_aliyev\n<b>Статус:</b> Защищенное соединение",
        
        "rename_prompt": "📝 Введите ваш <b>новый хакерский никнейм:</b>",
        "rename_success": "✅ Ваш никнейм успешно изменен на: <b>{}</b>"
    },
    "uz": {
        "welcome": "👋 <b>Spark CTF'ga xush kelibsiz!</b>\nSiz hali ro'yxatdan o'tmagansiz. Iltimos, <b>Hakerlik Nikingizni</b> kiriting:",
        "nickname_error": "⚠️ Nik 3 dan 15 ta gacha belgidan iborat bo'lishi kerak!",
        "lang_choose": "🌐 Iltimos, tilni tanlang:",
        "registered": "✅ <b>{}</b> nomi bilan muvaffaqiyatli ro'yxatdan o'tdingiz!",
        "welcome_back": "Qaytganingiz bilan, <b>{}</b>!",
        
        "btn_challenges": "🎯 Vazifalar",
        "btn_profile": "👤 Profil",
        "btn_ranking": "🏆 Reyting",
        "btn_info": "ℹ️ Info",
        
        "no_tasks": "Hozircha vazifalar mavjud emas.",
        "select_task": "Vazifani tanlang:",
        "task_format": "<b>{}</b>\nBallar: {} pts\n\nFormat: <code>SPARK{{flag_here}}</code>",
        "send_flag": "Ushbu vazifani ishlash uchun bayroqni (flag) yuboring.",
        "already_solved": "Siz bu vazifani allaqachon ishlagansiz! ✅",
        "wrong_flag": "❌ Noto'g'ri bayroq! Qaytadan urinib ko'ring.",
        "correct_flag": "🎉 To'g'ri! Siz {} pts oldingiz.",
        
        "profile_text": "👤 <b>PROFIL</b>\n\n<b>Nik:</b> {}\n<b>Ballar:</b> {} pts\n<b>Yechilgan:</b> {}",
        "ranking_empty": "🏆 <b>Global Reyting</b>\n\n<i>Hozircha reytingda hech kim yo'q...</i>",
        "ranking_title": "🏆 <b>Global Reyting</b>\n━━━━━━━━━━━━━━━━━━\n\n",
        "ranking_footer": "\n━━━━━━━━━━━━━━━━━━\n🎯 <i>Reytingda ko'tarilish uchun vazifalarni ishlashda davom eting!</i>",
        
        "info_text": "<b>SPARK CTF PLATFORMASI</b>\n\n<b>Bayroq formati:</b> <code>SPARK{flag_here}</code>\n<b>Nikni o'zgartirish:</b> /rename\n\n<b>Dasturchi:</b> @uchqun_aliyev\n<b>Holat:</b> Himoyalangan ulanish",
        
        "rename_prompt": "📝 <b>Yangi hakerlik nikingizni</b> kiriting:",
        "rename_success": "✅ Nikingiz muvaffaqiyatli o'zgartirildi: <b>{}</b>"
    }
}

def get_text(lang, key):
    return texts.get(lang, texts["en"]).get(key, texts["en"].get(key, ""))
