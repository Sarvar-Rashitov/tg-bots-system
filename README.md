# Telegram Downloader Bot - Django Admin Dashboard

A complete Telegram bot management platform built with Django MVT architecture. Manage multiple Telegram downloader bots, users, subscriptions, and broadcasts from a clean web dashboard.

## Features

- **Multi-Bot Management**: Add and manage multiple Telegram bots from one dashboard
- **Platform Support**: YouTube, Instagram, TikTok video downloads
- **Force Subscribe**: Require users to join channels before using the bot
- **Broadcast System**: Send messages/photos/videos to all users
- **Analytics Dashboard**: Real-time statistics and insights
- **File Cache**: Reuse previously downloaded videos (no duplicate uploads)
- **User Management**: Ban/unban users, view statistics

## Tech Stack

- Django 5 (MVT Architecture)
- SQLite3 (Database)
- aiogram 3 (Telegram Bot Framework)
- yt-dlp (Video Downloading)
- ffmpeg (Video Processing)

## Project Structure

```
telegram_downloader/
├── bots/              # Telegram bot management & handlers
├── users/             # User management
├── downloads/         # Download tracking & file caching
├── broadcasts/        # Broadcast messages
├── subscriptions/     # Force-subscribe channels
├── core/              # Dashboard & analytics
├── templates/         # HTML templates
├── static/            # CSS/JS/images
├── media/             # Uploaded/downloaded files
├── manage.py          # Django CLI
└── run_bot.py         # Standalone bot runner
```

## Installation & Setup

### Prerequisites

- Python 3.9+
- ffmpeg installed and in PATH
- Git (optional)

### Steps

1. **Clone/Download the project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup ffmpeg**
   - Windows: Download from https://ffmpeg.org/download.html and add to PATH
   - Linux: `sudo apt install ffmpeg`
   - Mac: `brew install ffmpeg`

4. **Create database**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Create media directories**
   ```bash
   mkdir -p media/downloads
   ```

7. **Add your Telegram Bot**
   - Talk to @BotFather on Telegram
   - Create a new bot and get the token
   - In Django admin, add a new TelegramBot with your token

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the dashboard**
   - Web: http://127.0.0.1:8000/admin
   - Bot: Start your bot in Telegram

## Running the Bot

### Option 1: From Django (development)
The bot runs as part of Django process (if using Django runserver with threaded option).

### Option 2: Standalone (recommended for production)
```bash
python run_bot.py
```

Or use Django management command:
```bash
python manage.py startbot
```

## Usage Guide

### Dashboard
View statistics: total users, downloads, platform breakdown, active bots.

### Bots
Add/edit/remove Telegram bots. Each bot works independently with its own token.

### Users
View all users, ban/unban, see download history per user.

### Channels
Configure force-subscribe channels. Users must join these before using the bot.

### Broadcasts
Create and send announcements to all users. Supports text, photos, videos.

### Downloads
View download history, filter by platform, search URLs.

## Bot Commands

- `/start` - Welcome message & menu
- `/help` - Usage instructions
- `/stats` - Your download statistics

Just send a YouTube/Instagram/TikTok link to download!

## Configuration

### Django Settings (`telegram_downloader/settings.py`)

```python
# Bot token (optional - can add via admin)
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# File upload limits
FILE_UPLOAD_MAX_MEMORY_SIZE = 104857600  # 100MB

# Download directory
DOWNLOAD_DIR = BASE_DIR / 'media' / 'downloads'
```

### Environment Variables (optional)

Create a `.env` file:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
DEBUG=True
```

## Database Models

- **TelegramBot** - Bot tokens and configuration
- **BotUser** - Telegram users
- **DownloadHistory** - Log of all downloads
- **SubscriptionChannel** - Force-subscribe channels
- **CachedFile** - Cached files by URL hash
- **BroadcastMessage** - Scheduled/broadcast messages

## File Cache System

The bot caches downloaded videos by URL hash. If someone requests the same URL again, it sends the cached Telegram file_id instead of re-downloading and re-uploading.

## Force Subscribe System

1. Add channels in Django admin
2. Set `is_required=True` for mandatory channels
3. Users will see subscription buttons before using the bot
4. Bot verifies membership via Telegram API

## Security Notes

- Never commit your bot tokens to version control
- Use environment variables in production
- Restrict admin panel to trusted users
- Consider rate limiting for download quotas

## Scaling Considerations

This is a starter project. For production scale:
- Replace SQLite with PostgreSQL
- Use Celery + Redis for background downloads
- Add rate limiting per user
- Use Telegram webhooks instead of polling
- Implement proper error monitoring
- Add CDN for file storage
- Use nginx + gunicorn/uWSGI

## Troubleshooting

**Bot not responding?**
- Check bot token in admin
- Ensure bot is marked active
- Check `run_bot.py` is running

**Downloads failing?**
- Verify ffmpeg is installed: `ffmpeg -version`
- Check URL is from supported platforms
- Ensure file size < 50MB (Telegram limit)

**ModuleNotFoundError?**
```bash
pip install -r requirements.txt
```

## Contributing

This is a beginner-friendly project. Contributions welcome!

## License

MIT License - Free to use and modify.

---

Made with ❤️ using Django & aiogram
