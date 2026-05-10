"""
Main Telegram Bot handler using aiogram 3
Supports YouTube, Instagram, TikTok downloads
"""

import asyncio
import hashlib
import logging
import os
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path

import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.enums import ParseMode
from asgiref.sync import sync_to_async

# Django setup
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')
django.setup()

from bots.models import TelegramBot
from users.models import BotUser
from downloads.models import DownloadHistory, CachedFile
from subscriptions.models import SubscriptionChannel
from downloads.downloader import VideoDownloader
from bots.language import get_text, get_language_keyboard, TEXTS

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global bot instances
active_bots = {}
dispatchers = {}


@sync_to_async
def get_or_create_user(user_id: int, username: str = '', first_name: str = '', last_name: str = ''):
    """Get or create user with default language"""
    user, created = BotUser.objects.get_or_create(
        telegram_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'language': 'en'  # Default language
        }
    )
    return user, created


@sync_to_async
def get_user_language(user_id: int) -> str:
    """Get user's language preference"""
    try:
        user = BotUser.objects.get(telegram_id=user_id)
        return user.language
    except BotUser.DoesNotExist:
        return 'en'


@sync_to_async
def set_user_language(user_id: int, language: str):
    """Set user's language preference"""
    try:
        user = BotUser.objects.get(telegram_id=user_id)
        user.language = language
        user.save()
        return True
    except BotUser.DoesNotExist:
        return False


def create_main_keyboard(language: str = 'en') -> InlineKeyboardMarkup:
    """Create main menu inline keyboard with localization"""
    keyboard = [
        [InlineKeyboardButton(text=get_text(language, 'youtube'), callback_data="platform_youtube")],
        [InlineKeyboardButton(text=get_text(language, 'instagram'), callback_data="platform_instagram")],
        [InlineKeyboardButton(text=get_text(language, 'tiktok'), callback_data="platform_tiktok")],
        [InlineKeyboardButton(text=get_text(language, 'about'), callback_data="about"),
         InlineKeyboardButton(text=get_text(language, 'stats'), callback_data="stats")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def create_subscription_keyboard(channels: list, language: str = 'en') -> InlineKeyboardMarkup:
    """Create inline keyboard with subscription buttons"""
    keyboard = []
    for channel in channels:
        keyboard.append([
            InlineKeyboardButton(
                text=f"📢 {channel.title}",
                url=f"https://t.me/{channel.channel_username.replace('@', '')}"
            )
        ])
    keyboard.append([
        InlineKeyboardButton(
            text=get_text(language, 'subscribed_button'),
            callback_data="check_subscription"
        )
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@sync_to_async
def _get_required_channels():
    """Synchronous helper to get required channels"""
    return list(SubscriptionChannel.objects.filter(is_required=True, is_active=True))


async def check_subscription(user_id: int, bot: Bot) -> tuple[bool, list]:
    """
    Check if user is subscribed to all required channels
    Returns (is_subscribed, list_of_missing_channels)
    """
    required_channels = await _get_required_channels()
    missing_channels = []
    
    logger.info(f"Checking subscription for user {user_id}")
    logger.info(f"Required channels: {[ch.channel_username for ch in required_channels]}")

    for channel in required_channels:
        try:
            logger.info(f"Checking channel: {channel.channel_username} (ID: {channel.channel_id})")
            member = await bot.get_chat_member(chat_id=channel.channel_id, user_id=user_id)
            logger.info(f"Member status for {channel.channel_username}: {member.status}")
            
            # User is subscribed if they have any of these statuses
            if member.status not in ['member', 'administrator', 'creator', 'restricted']:
                missing_channels.append(channel)
                logger.warning(f"User {user_id} NOT subscribed to {channel.channel_username}, status: {member.status}")
            else:
                logger.info(f"✅ User {user_id} subscribed to {channel.channel_username}, status: {member.status}")
        except Exception as e:
            logger.error(f"❌ Error checking subscription for {channel.channel_username} (ID: {channel.channel_id}): {e}")
            
            # Handle specific errors
            if "chat not found" in str(e).lower():
                logger.warning(f"Channel {channel.channel_username} not accessible - may be deleted or bot removed")
                # Skip this channel instead of blocking user
                continue
            else:
                # For other errors, assume user is not subscribed
                missing_channels.append(channel)

    return len(missing_channels) == 0, missing_channels


@sync_to_async
def get_bot_token():
    """Get the first active bot token from database"""
    bot = TelegramBot.objects.filter(is_active=True).first()
    if bot:
        return bot.token
    return None


@sync_to_async
def _get_required_channels():
    """Synchronous helper to get required channels"""
    return list(SubscriptionChannel.objects.filter(is_required=True, is_active=True))


async def start_command(message: Message, bot: Bot):
    """Handle /start command with language selection"""
    user = message.from_user

    # Get or create user
    bot_user, created = await get_or_create_user(
        user.id,
        user.username or '',
        user.first_name or '',
        user.last_name or ''
    )

    # If new user or no language set, show language selection
    if created or not bot_user.language:
        text = get_text('en', 'choose_language')
        keyboard = get_language_keyboard()
        await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return

    # Update last activity
    @sync_to_async
    def update_activity():
        bot_user.last_activity = datetime.now()
        bot_user.save()

    await update_activity()

    # Get user's language
    user_language = await get_user_language(user.id)

    # Check subscription
    is_subscribed, missing_channels = await check_subscription(user.id, bot)

    if not is_subscribed:
        text = get_text(user_language, 'required_channels')
        channel_list = ""
        for channel in missing_channels:
            channel_list += f"• @{channel.channel_username.replace('@', '')}\n"
        text = text.format(channel_list)

        keyboard = create_subscription_keyboard(missing_channels, user_language)
        await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return

    # Welcome message with platform selection
    welcome_text = get_text(user_language, 'welcome')
    platform_text = get_text(user_language, 'select_platform')
    
    await message.answer(welcome_text, parse_mode=ParseMode.HTML)
    await message.answer(platform_text, reply_markup=create_main_keyboard(user_language), parse_mode=ParseMode.HTML)


async def language_command(message: Message):
    """Handle /language command"""
    text = get_text('en', 'choose_language')
    keyboard = get_language_keyboard()
    await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


async def help_command(message: Message):
    """Handle /help command"""
    user_language = await get_user_language(message.from_user.id)
    text = get_text(user_language, 'help_text')
    await message.answer(text, parse_mode=ParseMode.HTML)


async def stats_command(message: Message):
    """Show user statistics"""
    user_language = await get_user_language(message.from_user.id)
    
    @sync_to_async
    def get_user_stats():
        try:
            user = BotUser.objects.get(telegram_id=message.from_user.id)
            downloads = DownloadHistory.objects.filter(user=user).count()
            return user, downloads
        except BotUser.DoesNotExist:
            return None, 0

    user, downloads = await get_user_stats()
    
    if not user:
        text = get_text(user_language, 'user_not_found')
        await message.answer(text)
        return
        
    text = get_text(user_language, 'stats_text', 
                   downloads,
                   user.joined_at.strftime('%d %b %Y'),
                   user.last_activity.strftime('%d %b %Y %H:%M'))
    await message.answer(text, parse_mode=ParseMode.HTML)


async def process_url_download(url: str, user_id: int, bot: Bot, reply_func, reply_video_func):
    """Process URL download - separate function for reuse"""
    
    # Get user language
    user_language = await get_user_language(user_id)

    # Get or update user
    bot_user, created = await get_or_create_user(
        user_id,
        '',  # username will be updated if needed
        '',  # first_name will be updated if needed
        ''   # last_name will be updated if needed
    )

    # Update last activity and save URL
    @sync_to_async
    def update_activity_and_url():
        bot_user.last_activity = datetime.now()
        bot_user.last_url = url
        bot_user.save()

    await update_activity_and_url()

    # Detect platform
    platform = detect_platform(url)
    if not platform:
        text = get_text(user_language, 'unsupported_url')
        await reply_func(text)
        return

    # Send loading message
    loading_text = get_text(user_language, 'processing', platform)
    loading_msg = await reply_func(loading_text)

    try:
        # Check cache first
        url_hash = hashlib.sha256(url.encode()).hexdigest()
        
        @sync_to_async
        def check_cache():
            return CachedFile.objects.filter(url_hash=url_hash).first()

        cached = await check_cache()

        if cached and os.path.exists(cached.file_path):
            logger.info(f"Cache hit for URL: {url[:50]}")
            # Resend from Telegram
            await loading_msg.edit_text(get_text(user_language, 'uploading'))

            try:
                if cached.telegram_file_id:
                    # Directly send using file_id (avoids re-upload)
                    success_text = get_text(user_language, 'success', platform)
                    await reply_video_func(
                        video=cached.telegram_file_id,
                        caption=success_text,
                        parse_mode=ParseMode.HTML
                    )
                else:
                    # Fallback: send from file
                    success_text = get_text(user_language, 'success', platform)
                    await reply_video_func(
                        video=types.FSInputFile(cached.file_path),
                        caption=success_text,
                        parse_mode=ParseMode.HTML
                    )

                @sync_to_async
                def save_cache_and_history():
                    cached.download_count += 1
                    cached.save()
                    # Record download history
                    DownloadHistory.objects.create(
                        user=bot_user,
                        platform=platform,
                        url=url,
                        file_path=cached.file_path,
                        file_size=cached.file_size,
                        telegram_file_id=cached.telegram_file_id
                    )
                    bot_user.download_count += 1
                    bot_user.save()

                await save_cache_and_history()
                await loading_msg.delete()
                
                # Show platform selection again
                platform_text = get_text(user_language, 'select_platform')
                await reply_func(platform_text, reply_markup=create_main_keyboard(user_language), parse_mode=ParseMode.HTML)
                return
            except Exception as e:
                logger.error(f"Error sending cached file: {e}")
                # Fall through to re-download

        # Download new file
        await loading_msg.edit_text(get_text(user_language, 'downloading', platform))

        downloader = VideoDownloader()
        file_path, file_size, thumbnail = await downloader.download(url, platform)

        if not file_path or not os.path.exists(file_path):
            error_text = get_text(user_language, 'error_private')
            await loading_msg.edit_text(error_text)
            return

        # Upload to Telegram
        await loading_msg.edit_text(get_text(user_language, 'uploading'))

        # Check file size (Telegram limit ~50MB for bots)
        if file_size > 50 * 1024 * 1024:
            error_text = get_text(user_language, 'error_large')
            await loading_msg.edit_text(error_text)
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        # Upload video with high quality
        with open(file_path, 'rb') as video_file:
            success_text = get_text(user_language, 'success', platform)
            sent_message = await reply_video_func(
                video=types.FSInputFile(file_path),
                caption=success_text,
                parse_mode=ParseMode.HTML,
                width=1920,  # High quality settings
                height=1080,
                supports_streaming=True
            )

        # Get Telegram file_id
        telegram_file_id = sent_message.video.file_id

        # Cache the file and record history
        @sync_to_async
        def save_new_download():
            CachedFile.objects.create(
                url_hash=url_hash,
                original_url=url,
                file_id=telegram_file_id,
                file_path=file_path,
                file_size=file_size
            )
            # Record download history
            DownloadHistory.objects.create(
                user=bot_user,
                platform=platform,
                url=url,
                file_path=file_path,
                file_size=file_size,
                telegram_file_id=telegram_file_id
            )
            bot_user.download_count += 1
            bot_user.save()

        await save_new_download()
        await loading_msg.delete()
        
        # Show platform selection again
        platform_text = get_text(user_language, 'select_platform')
        await reply_func(platform_text, reply_markup=create_main_keyboard(user_language), parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(f"Download error: {e}", exc_info=True)
        error_text = get_text(user_language, 'error_general', str(e)[:100])
        await loading_msg.edit_text(error_text)


async def handle_url(message: Message, bot: Bot):
    """Handle URL messages - detect platform and download"""
    user = message.from_user
    url = message.text.strip()

    # Get user language
    user_language = await get_user_language(user.id)

    # Check subscription first
    is_subscribed, missing_channels = await check_subscription(user.id, bot)
    if not is_subscribed:
        # Update user info and save URL
        bot_user, created = await get_or_create_user(
            user.id,
            user.username or '',
            user.first_name or '',
            user.last_name or ''
        )
        
        @sync_to_async
        def save_url():
            bot_user.last_url = url
            bot_user.save()
        
        await save_url()
        
        text = get_text(user_language, 'required_channels')
        channel_list = ""
        for channel in missing_channels:
            channel_list += f"• @{channel.channel_username.replace('@', '')}\n"
        text = text.format(channel_list)
        
        keyboard = create_subscription_keyboard(missing_channels, user_language)
        await message.answer(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)
        return

    # Process download
    await process_url_download(
        url, 
        user.id, 
        bot,
        message.answer,
        message.answer_video
    )


def detect_platform(url: str) -> str | None:
    """Detect which platform the URL belongs to"""
    url = url.lower()

    if 'youtube.com' in url or 'youtu.be' in url:
        return 'YOUTUBE'
    elif 'instagram.com' in url:
        return 'INSTAGRAM'
    elif 'tiktok.com' in url:
        return 'TIKTOK'
    else:
        return None


async def button_callback(callback_query: types.CallbackQuery, bot: Bot):
    """Handle inline button callbacks"""
    await callback_query.answer()

    data = callback_query.data
    message = callback_query.message
    user = callback_query.from_user
    
    # Get user language
    user_language = await get_user_language(user.id)

    # Handle language selection
    if data.startswith("lang_"):
        language = data.split("_")[1]
        await set_user_language(user.id, language)
        
        # Send language confirmation
        text = get_text(language, 'language_set')
        await message.edit_text(text)
        
        # Show welcome message
        welcome_text = get_text(language, 'welcome')
        platform_text = get_text(language, 'select_platform')
        
        await bot.send_message(
            chat_id=user.id,
            text=welcome_text,
            parse_mode=ParseMode.HTML
        )
        await bot.send_message(
            chat_id=user.id,
            text=platform_text,
            reply_markup=create_main_keyboard(language),
            parse_mode=ParseMode.HTML
        )
        return

    elif data == "check_subscription":
        # Re-check subscription
        is_subscribed, missing_channels = await check_subscription(user.id, bot)

        if is_subscribed:
            # Update user status and get last URL
            @sync_to_async
            def mark_subscribed_and_get_url():
                user_obj = BotUser.objects.get(telegram_id=user.id)
                user_obj.is_subscribed = True
                last_url = user_obj.last_url
                user_obj.save()
                return last_url

            last_url = await mark_subscribed_and_get_url()

            verified_text = get_text(user_language, 'verified')
            await message.edit_text(verified_text)

            # Agar oxirgi URL mavjud bo'lsa, uni avtomatik yuklab berish
            if last_url:
                # URL ni qayta ishlab berish
                await process_url_download(
                    last_url,
                    user.id,
                    bot,
                    lambda text, **kwargs: bot.send_message(user.id, text, **kwargs),
                    lambda **kwargs: bot.send_video(user.id, **kwargs)
                )
            else:
                # Agar URL yo'q bo'lsa, platforma tanlashni ko'rsatish
                platform_text = get_text(user_language, 'select_platform')
                await bot.send_message(
                    chat_id=user.id,
                    text=platform_text,
                    reply_markup=create_main_keyboard(user_language),
                    parse_mode=ParseMode.HTML
                )
        else:
            text = get_text(user_language, 'not_subscribed')
            await message.edit_text(text)

    elif data == "about":
        text = get_text(user_language, 'about_text')
        
        # Ortga qaytish tugmasi
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, 'back'), callback_data="back_to_main")]
        ])
        
        await message.edit_text(text, reply_markup=back_keyboard, parse_mode=ParseMode.HTML)

    elif data == "stats":
        @sync_to_async
        def get_user_for_stats():
            try:
                return BotUser.objects.get(telegram_id=user.id)
            except BotUser.DoesNotExist:
                return None

        bot_user = await get_user_for_stats()
        
        if not bot_user:
            text = get_text(user_language, 'user_not_found')
            await message.edit_text(text)
            return
            
        text = get_text(user_language, 'stats_text',
                       bot_user.download_count,
                       bot_user.joined_at.strftime('%d %b %Y'),
                       bot_user.last_activity.strftime('%d %b %Y %H:%M'))
        
        # Ortga qaytish tugmasi
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, 'back'), callback_data="back_to_main")]
        ])
        
        await message.edit_text(text, reply_markup=back_keyboard, parse_mode=ParseMode.HTML)

    elif data == "back_to_main":
        # Asosiy menyuga qaytish
        platform_text = get_text(user_language, 'select_platform')
        await message.edit_text(
            platform_text, 
            reply_markup=create_main_keyboard(user_language), 
            parse_mode=ParseMode.HTML
        )

    elif data.startswith("platform_"):
        platform = data.split("_")[1].upper()
        text = get_text(user_language, 'send_link', platform)
        
        # Ortga qaytish tugmasi
        back_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=get_text(user_language, 'back'), callback_data="back_to_main")]
        ])
        
        await message.edit_text(text, reply_markup=back_keyboard, parse_mode=ParseMode.HTML)


def is_supported_url(message: Message) -> bool:
    """Check if message contains a supported URL"""
    if not message.text:
        return False
    text = message.text.lower()
    return any(platform in text for platform in ['youtube.com', 'youtu.be', 'instagram.com', 'tiktok.com'])


async def start_bot_for_token(token: str):
    """Start a bot instance with given token"""
    try:
        bot = Bot(token=token, parse_mode=ParseMode.HTML)
        dp = Dispatcher()

        # Register handlers
        dp.message.register(start_command, CommandStart())
        dp.message.register(help_command, Command("help"))
        dp.message.register(stats_command, Command("stats"))
        dp.message.register(language_command, Command("language"))
        # Register URL handler with custom filter
        dp.message.register(handle_url, is_supported_url)
        dp.callback_query.register(button_callback)

        # Fallback for any text
        @dp.message()
        async def fallback_handler(message: Message):
            user_language = await get_user_language(message.from_user.id)
            
            if message.text and ('youtube.com' in message.text.lower() or 'youtu.be' in message.text.lower() or
                                 'instagram.com' in message.text.lower() or 'tiktok.com' in message.text.lower()):
                await handle_url(message, bot)
            else:
                platform_text = get_text(user_language, 'select_platform')
                await message.answer(
                    platform_text,
                    reply_markup=create_main_keyboard(user_language),
                    parse_mode=ParseMode.HTML
                )

        # Store bot and dispatcher
        active_bots[token] = bot
        dispatchers[token] = dp

        logger.info(f"Bot started with token: {token[:10]}...")

        # Start polling
        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Failed to start bot: {e}")


async def shutdown_bot(token: str):
    """Stop a bot instance"""
    if token in active_bots:
        bot = active_bots[token]
        await bot.session.close()
        del active_bots[token]
        if token in dispatchers:
            del dispatchers[token]
        logger.info(f"Bot stopped: {token[:10]}...")


async def main():
    """Main entry point - start all active bots"""
    logger.info("Starting Telegram Downloader Bot Service...")

    @sync_to_async
    def get_active_tokens():
        return list(TelegramBot.objects.filter(is_active=True).values_list('token', flat=True))

    while True:
        try:
            # Get all active bots from database
            active_tokens = await get_active_tokens()

            # Start new bots
            for token in active_tokens:
                if token not in active_bots:
                    asyncio.create_task(start_bot_for_token(token))

            # Stop removed bots
            for token in list(active_bots.keys()):
                if token not in active_tokens:
                    await shutdown_bot(token)

            await asyncio.sleep(30)  # Check every 30 seconds

        except KeyboardInterrupt:
            logger.info("Shutting down...")
            for token in list(active_bots.keys()):
                await shutdown_bot(token)
            break
        except Exception as e:
            logger.error(f"Main loop error: {e}")
            await asyncio.sleep(30)


if __name__ == '__main__':
    asyncio.run(main())
