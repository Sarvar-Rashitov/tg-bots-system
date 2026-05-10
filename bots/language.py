"""
Bot language support
"""

# Language texts
TEXTS = {
    'en': {
        'choose_language': '🌐 Choose your language / Выберите язык / Tilni tanlang',
        'language_set': '✅ Language set to English',
        'welcome': '''👋 <b>Welcome!</b>

I'm a powerful media downloader bot that can download videos from:

• <b>YouTube</b> - Videos, Shorts, Playlists
• <b>Instagram</b> - Reels, Posts, Stories  
• <b>TikTok</b> - Videos, Slideshows

<b>How to use:</b>
Just send me any link from these platforms and I'll download it for you!

Select a platform below or send a link directly.''',
        'select_platform': '📱 Select a platform to download from:',
        'youtube': '🎬 YouTube',
        'instagram': '📸 Instagram', 
        'tiktok': '🎵 TikTok',
        'about': 'ℹ️ About',
        'stats': '📊 Stats',
        'back': '🔙 Back',
        'required_channels': '''📢 <b>Required Channels</b>

Please subscribe to the following channels to use this bot:

{}

After subscribing, click 'I've Subscribed' below.''',
        'subscribed_button': "✅ I've Subscribed",
        'not_subscribed': "⚠️ You still need to subscribe to the channels above.",
        'verified': "✅ You're verified! Welcome!",
        'processing': "⏳ Processing {} link...",
        'downloading': "⬇️ Downloading {} video...",
        'uploading': "📤 Uploading to Telegram...",
        'success': "✅ <b>{} Video</b>\n\nDownloaded successfully!",
        'error_private': "❌ Failed to download. Video may be private or restricted.",
        'error_large': "❌ File too large (>50MB). Telegram bot limit.",
        'error_general': "❌ Error: {}",
        'unsupported_url': "❌ Unsupported URL. Please send YouTube, Instagram, or TikTok links.",
        'send_link': "Send me a {} video link and I'll download it for you!\n\nExample URLs:\n• https://youtube.com/watch?v=...\n• https://instagram.com/reel/...\n• https://tiktok.com/@.../video/...",
        'help_text': '''🆘 <b>Help</b>

<b>Supported URLs:</b>
• YouTube: youtube.com, youtu.be
• Instagram: instagram.com
• TikTok: tiktok.com

<b>Commands:</b>
/start - Start the bot
/help - Show this help
/stats - Show your statistics
/language - Change language

<b>Limits:</b>
Max file size: 50MB (Telegram limit)''',
        'stats_text': '''📊 <b>Your Statistics</b>

<b>Total Downloads:</b> {}
<b>Account Created:</b> {}
<b>Last Activity:</b> {}''',
        'about_text': '''🤖 <b>Telegram Downloader Bot</b>

<b>Version:</b> 1.0.0
<b>Features:</b>
• Download videos from YouTube, Instagram, TikTok
• Fast downloads with progress updates
• File caching for repeat downloads
• No watermarks

<b>Limits:</b>
• Max file size: 50MB
• Downloads per user: Unlimited

Made with ❤️ using Django & aiogram''',
        'user_not_found': "❌ User not found. Please use /start first."
    },
    'ru': {
        'choose_language': '🌐 Choose your language / Выберите язык / Tilni tanlang',
        'language_set': '✅ Язык установлен на русский',
        'welcome': '''👋 <b>Добро пожаловать!</b>

Я мощный бот для загрузки медиа, который может скачивать видео с:

• <b>YouTube</b> - Видео, Shorts, Плейлисты
• <b>Instagram</b> - Reels, Посты, Stories
• <b>TikTok</b> - Видео, Слайдшоу

<b>Как использовать:</b>
Просто отправьте мне любую ссылку с этих платформ, и я скачаю её для вас!

Выберите платформу ниже или отправьте ссылку напрямую.''',
        'select_platform': '📱 Выберите платформу для загрузки:',
        'youtube': '🎬 YouTube',
        'instagram': '📸 Instagram',
        'tiktok': '🎵 TikTok', 
        'about': 'ℹ️ О боте',
        'stats': '📊 Статистика',
        'back': '🔙 Назад',
        'required_channels': '''📢 <b>Обязательные каналы</b>

Пожалуйста, подпишитесь на следующие каналы для использования бота:

{}

После подписки нажмите 'Я подписался' ниже.''',
        'subscribed_button': "✅ Я подписался",
        'not_subscribed': "⚠️ Вам всё ещё нужно подписаться на каналы выше.",
        'verified': "✅ Вы верифицированы! Добро пожаловать!",
        'processing': "⏳ Обрабатываю {} ссылку...",
        'downloading': "⬇️ Скачиваю {} видео...",
        'uploading': "📤 Загружаю в Telegram...",
        'success': "✅ <b>{} Видео</b>\n\nУспешно скачано!",
        'error_private': "❌ Не удалось скачать. Видео может быть приватным или ограниченным.",
        'error_large': "❌ Файл слишком большой (>50МБ). Лимит Telegram бота.",
        'error_general': "❌ Ошибка: {}",
        'unsupported_url': "❌ Неподдерживаемая ссылка. Отправьте ссылки YouTube, Instagram или TikTok.",
        'send_link': "Отправьте мне {} видео ссылку и я скачаю её для вас!\n\nПримеры ссылок:\n• https://youtube.com/watch?v=...\n• https://instagram.com/reel/...\n• https://tiktok.com/@.../video/...",
        'help_text': '''🆘 <b>Помощь</b>

<b>Поддерживаемые ссылки:</b>
• YouTube: youtube.com, youtu.be
• Instagram: instagram.com
• TikTok: tiktok.com

<b>Команды:</b>
/start - Запустить бота
/help - Показать эту помощь
/stats - Показать вашу статистику
/language - Изменить язык

<b>Лимиты:</b>
Максимальный размер файла: 50МБ (лимит Telegram)''',
        'stats_text': '''📊 <b>Ваша статистика</b>

<b>Всего загрузок:</b> {}
<b>Аккаунт создан:</b> {}
<b>Последняя активность:</b> {}''',
        'about_text': '''🤖 <b>Telegram Downloader Bot</b>

<b>Версия:</b> 1.0.0
<b>Возможности:</b>
• Загрузка видео с YouTube, Instagram, TikTok
• Быстрые загрузки с обновлениями прогресса
• Кэширование файлов для повторных загрузок
• Без водяных знаков

<b>Лимиты:</b>
• Максимальный размер файла: 50МБ
• Загрузок на пользователя: Неограниченно

Сделано с ❤️ используя Django & aiogram''',
        'user_not_found': "❌ Пользователь не найден. Используйте /start сначала."
    },
    'uz': {
        'choose_language': '🌐 Choose your language / Выберите язык / Tilni tanlang',
        'language_set': "✅ Til o'zbek tiliga o'rnatildi",
        'welcome': '''👋 <b>Xush kelibsiz!</b>

Men quyidagi platformalardan videolarni yuklab oluvchi kuchli botman:

• <b>YouTube</b> - Videolar, Shorts, Pleylistlar
• <b>Instagram</b> - Reels, Postlar, Stories
• <b>TikTok</b> - Videolar, Slaydshowlar

<b>Qanday foydalanish:</b>
Menga ushbu platformalardan istalgan havolani yuboring va men uni siz uchun yuklab beraman!

Quyidagi platformani tanlang yoki to'g'ridan-to'g'ri havola yuboring.''',
        'select_platform': '📱 Yuklab olish uchun platformani tanlang:',
        'youtube': '🎬 YouTube',
        'instagram': '📸 Instagram',
        'tiktok': '🎵 TikTok',
        'about': 'ℹ️ Bot haqida',
        'stats': '📊 Statistika',
        'back': '🔙 Ortga',
        'required_channels': '''📢 <b>Majburiy kanallar</b>

Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:

{}

Obuna bo'lganingizdan so'ng, quyidagi "Obuna bo'ldim" tugmasini bosing.''',
        'subscribed_button': "✅ Obuna bo'ldim",
        'not_subscribed': "⚠️ Siz hali ham yuqoridagi kanallarga obuna bo'lishingiz kerak.",
        'verified': "✅ Siz tasdiqlangansiz! Xush kelibsiz!",
        'processing': "⏳ {} havolasini qayta ishlamoqda...",
        'downloading': "⬇️ {} videosini yuklab olmoqda...",
        'uploading': "📤 Telegramga yuklash...",
        'success': "✅ <b>{} Video</b>\n\nMuvaffaqiyatli yuklab olindi!",
        'error_private': "❌ Yuklab olib bo'lmadi. Video shaxsiy yoki cheklangan bo'lishi mumkin.",
        'error_large': "❌ Fayl juda katta (>50MB). Telegram bot chegarasi.",
        'error_general': "❌ Xatolik: {}",
        'unsupported_url': "❌ Qo'llab-quvvatlanmaydigan havola. YouTube, Instagram yoki TikTok havolalarini yuboring.",
        'send_link': "Menga {} video havolasini yuboring va men uni siz uchun yuklab beraman!\n\nMisol havolalar:\n• https://youtube.com/watch?v=...\n• https://instagram.com/reel/...\n• https://tiktok.com/@.../video/...",
        'help_text': '''🆘 <b>Yordam</b>

<b>Qo'llab-quvvatlanadigan havolalar:</b>
• YouTube: youtube.com, youtu.be
• Instagram: instagram.com
• TikTok: tiktok.com

<b>Buyruqlar:</b>
/start - Botni ishga tushirish
/help - Ushbu yordamni ko'rsatish
/stats - Statistikangizni ko'rsatish
/language - Tilni o'zgartirish

<b>Cheklovlar:</b>
Maksimal fayl hajmi: 50MB (Telegram chegarasi)''',
        'stats_text': '''📊 <b>Sizning statistikangiz</b>

<b>Jami yuklanmalar:</b> {}
<b>Hisob yaratilgan:</b> {}
<b>So'nggi faollik:</b> {}''',
        'about_text': '''🤖 <b>Telegram Downloader Bot</b>

<b>Versiya:</b> 1.0.0
<b>Imkoniyatlar:</b>
• YouTube, Instagram, TikTok'dan videolarni yuklab olish
• Tez yuklanishlar va jarayon yangilanishlari
• Takroriy yuklanishlar uchun fayl keshlash
• Suv belgilarsiz

<b>Cheklovlar:</b>
• Maksimal fayl hajmi: 50MB
• Foydalanuvchi uchun yuklanishlar: Cheksiz

❤️ bilan Django & aiogram yordamida yaratilgan''',
        'user_not_found': "❌ Foydalanuvchi topilmadi. Avval /start dan foydalaning."
    }
}

def get_text(user_language: str, key: str, *args) -> str:
    """Get localized text"""
    lang = user_language if user_language in TEXTS else 'en'
    text = TEXTS[lang].get(key, TEXTS['en'].get(key, key))
    
    if args:
        return text.format(*args)
    return text

def get_language_keyboard():
    """Get language selection keyboard"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = [
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)