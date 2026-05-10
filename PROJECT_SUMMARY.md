# Telegram Downloader Bot - Complete Project

## Project Overview

A production-ready Telegram bot management platform built with pure Django MVT architecture. This system allows you to manage multiple Telegram downloader bots from a centralized web dashboard.

**Tech Stack:** Django 5, SQLite3, aiogram 3, yt-dlp, ffmpeg

**Key Principles:** Simple, Clean, Beginner-Friendly, Easy to Run Locally

---

## Complete Feature List

### ✅ 1. Multi-Bot Management
- Add unlimited Telegram bots from the dashboard
- Each bot operates independently with its own token
- Activate/deactivate bots instantly
- Bot username tracking

### ✅ 2. Smart Video Downloader
- **Platform Detection:** Auto-detects YouTube, Instagram, TikTok URLs
- **Download Engine:** yt-dlp for reliable downloading
- **Video Processing:** ffmpeg for format conversion
- **Progress Updates:** Real-time status messages in Telegram
- **File Size Validation:** Prevents files > 50MB (Telegram limit)

### ✅ 3. Force-Subscribe System
- Add multiple subscription channels
- Required vs optional channels
- Real-time membership verification
- Inline keyboard with join links
- "I've Subscribed" verification button

### ✅ 4. Broadcast Messaging
- Send messages to all users
- Support: Text, Photos, Videos
- Simple scheduling (send now or schedule)
- Progress tracking (sent/failed counters)
- Works via background threads (no Celery needed)

### ✅ 5. User Management
- View all bot users
- Search and filter (banned/active)
- Ban/unban users
- View individual user stats
- See download history per user
- Last activity tracking

### ✅ 6. Analytics Dashboard
- Total users, active users, banned users
- Total downloads count
- Platform breakdown (YouTube/Instagram/TikTok)
- Most used platform indicator
- Active bot count
- Recent downloads table

### ✅ 7. File Cache System
- URL-based caching (SHA256 hash)
- Telegram file_id storage
- Instant repeat downloads (no re-upload)
- Reduces bandwidth and server load
- Automatic cache hit detection

### ✅ 8. Modern Bot UX
- Beautiful start message with inline menu
- Platform selection buttons
- Loading animations during download
- Success/error notifications
- /stats command for users
- Clean, professional interface

---

## Project Structure

```
save bot/                         # Project root
├── manage.py                     # Django CLI entry point
├── run_bot.py                    # Standalone bot runner
├── requirements.txt              # Python dependencies
├── README.md                     # Main documentation
├── QUICKSTART.md                 # 5-minute setup guide
├── ARCHITECTURE.md               # Technical architecture
├── PROJECT_SUMMARY.md            # This file
├── .gitignore                    # Git ignore rules
├── .env.example                  # Environment template
│
├── telegram_downloader/          # Django project
│   ├── __init__.py
│   ├── settings.py               # Main configuration
│   ├── urls.py                   # Root URLs
│   └── wsgi.py                   # WSGI application
│
├── core/                         # Dashboard & analytics
│   ├── __init__.py
│   ├── admin.py                  # Django admin
│   ├── apps.py
│   ├── models.py                 # (none - uses other models)
│   ├── views.py                  # Dashboard view
│   ├── urls.py
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── custom_filters.py     # Template filters (percentage, filesize)
│   └── templates/
│       └── dashboard.html        # Main analytics page
│
├── bots/                         # Telegram bot management
│   ├── __init__.py
│   ├── admin.py                  # Bot admin interface
│   ├── apps.py
│   ├── models.py                 # TelegramBot model
│   ├── views.py                  # CRUD views
│   ├── urls.py                   # /bots/
│   ├── bot.py                    # Aiogram bot logic ★ MAIN BOT
│   ├── downloader.py             # (symlinked to downloads/)
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── startbot.py       # Django management command
│   ├── migrations/               # Database migrations
│   └── templates/
│       ├── bots/
│       │   ├── list.html
│       │   ├── form.html
│       │   └── confirm_delete.html
│
├── users/                        # User management
│   ├── __init__.py
│   ├── admin.py                  # User admin interface
│   ├── apps.py
│   ├── models.py                 # BotUser model
│   ├── views.py                  # List, detail, toggle ban
│   ├── urls.py                   # /users/
│   ├── migrations/
│   └── templates/
│       └── users/
│           ├── list.html
│           ├── detail.html
│           └── confirm_delete.html
│
├── downloads/                    # Download tracking & services
│   ├── __init__.py
│   ├── admin.py                  # History & cache admin
│   ├── apps.py
│   ├── models.py                 # DownloadHistory, CachedFile
│   ├── views.py                  # History list view
│   ├── urls.py                   # /downloads/
│   ├── downloader.py             # VideoDownloader class ★ CORE LOGIC
│   ├── migrations/
│   └── templates/
│       └── downloads/
│           └── history.html
│
├── broadcasts/                   # Mass messaging
│   ├── __init__.py
│   ├── admin.py                  # Broadcast admin
│   ├── apps.py
│   ├── models.py                 # BroadcastMessage model
│   ├── views.py                  # CRUD + send view
│   ├── urls.py                   # /broadcasts/
│   ├── migrations/
│   └── templates/
│       └── broadcasts/
│           ├── list.html
│           ├── form.html
│           ├── confirm_delete.html
│           └── send.html
│
├── subscriptions/                # Force-subscribe channels
│   ├── __init__.py
│   ├── admin.py                  # Channel admin
│   ├── apps.py
│   ├── models.py                 # SubscriptionChannel model
│   ├── views.py                  # CRUD views
│   ├── urls.py                   # /subscriptions/
│   ├── migrations/
│   └── templates/
│       └── subscriptions/
│           ├── list.html
│           ├── form.html
│           └── confirm_delete.html
│
├── templates/                    # Global templates
│   ├── base.html                 # Base template with sidebar
│   └── partials/
│       └── sidebar.html          # Navigation sidebar
│
├── static/                       # Static assets
│   └── custom.css                # Custom CSS styles
│
└── media/                        # Uploaded/downloaded files
    └── downloads/                # Temporary video storage
```

---

## Database Models

### 1. TelegramBot
```python
- token (CharField, unique)         # Bot token from @BotFather
- username (CharField)              # Bot username (without @)
- bot_owner (FK -> User, optional)  # Django user who owns bot
- is_active (Boolean)               # Enable/disable bot
- created_at, updated_at (DateTime)
```

### 2. BotUser
```python
- telegram_id (BigInteger, unique)  # Telegram user ID
- username (CharField, blank)       # Telegram @username
- first_name, last_name (CharField) # User's name
- is_banned (Boolean)               # Ban status
- is_subscribed (Boolean)           # Force-subscribe status
- download_count (Integer)          # Total downloads by user
- joined_at, last_activity (DateTime)
```

### 3. DownloadHistory
```python
- user (FK -> BotUser)             # Who downloaded
- platform (Char: YOUTUBE/INSTAGRAM/TIKTOK)
- url (TextField)                  # Original URL
- file_path (CharField, blank)     # Local file path
- file_size (BigInteger)           # Size in bytes
- downloaded_at (DateTime)         # When downloaded
- telegram_file_id (CharField)     # Telegram's file_id for caching
```

### 4. CachedFile
```python
- url_hash (CharField, unique)      # SHA256 of URL
- original_url (TextField)          # Original URL
- file_id (CharField)               # Telegram file_id
- file_path (CharField)             # Local storage path
- file_size (BigInteger)            # Size in bytes
- download_count (Integer)          # How many times reused
- created_at, last_used (DateTime)
```

### 5. SubscriptionChannel
```python
- channel_id (BigInteger, unique)   # Telegram channel numeric ID
- channel_username (CharField, unique) # @channelname
- title (CharField)                 # Display name
- invite_link (CharField, blank)    # Join link
- is_required (Boolean)             # Mandatory or optional
- is_active (Boolean)               # Enable/disable
- added_at (DateTime)
```

### 6. BroadcastMessage
```python
- title (CharField)                 # Broadcast title
- message (TextField)               # Message content
- message_type (Char: TEXT/PHOTO/VIDEO)
- media_file (FileField, optional)  # Attached media
- total_users (Integer)             # Target audience size
- sent_count, failed_count (Integer)# Progress tracking
- is_scheduled (Boolean)            # Schedule flag
- scheduled_at (DateTime, nullable) # When to send
- created_at (DateTime)             # Creation timestamp
- created_by (FK -> User)           # Admin who created
```

---

## Bot Workflow

### User Journey

```
1. START Command
   → Bot checks user in DB (creates if new)
   → Checks force-subscribe channels
   → NOT SUBSCRIBED → Show join buttons
   → SUBSCRIBED → Show main menu

2. Send URL
   → Bot detects platform (YouTube/Instagram/TikTok)
   → Calculate URL SHA256 hash
   → Check CachedFile for hash
   → CACHED → Resend via file_id (instant!)
   → NOT CACHED → Download with yt-dlp

3. Download Process
   → yt-dlp fetches best quality < 50MB
   → ffmpeg converts to MP4 (if needed)
   → Upload to Telegram
   → Get Telegram file_id
   → Save to CachedFile & DownloadHistory
   → Update user's download_count
   → Send video to user

4. Statistics Update
   → Dashboard updates automatically (refresh)
   → User stats increment
   → Platform counts increment
```

### Broadcast Flow

```
1. Admin creates broadcast in dashboard
2. Clicks "Send Now" → Creates broadcast record
3. Background thread starts
4. Gets all non-banned users
5. For each user:
   - Sends message (with 50ms delay)
   - Updates sent_count
   - Logs errors
6. Mark broadcast as completed
7. Dashboard shows progress
```

---

## URL Routing

### Root URLs (`telegram_downloader/urls.py`)
| Path | View | Description |
|------|------|-------------|
| `/admin/` | Django Admin | Admin panel |
| `/` | `core.views.dashboard` | Analytics dashboard |
| `/bots/` | `bots.urls` | Bot management |
| `/users/` | `users.urls` | User management |
| `/downloads/history/` | `downloads.urls` | Download logs |
| `/broadcasts/` | `broadcasts.urls` | Message broadcasts |
| `/subscriptions/` | `subscriptions.urls` | Force-subscribe channels |

### Bots URLs (`bots/urls.py`)
| Path | View | Description |
|------|------|-------------|
| `/bots/` | ListView | List all bots |
| `/bots/add/` | CreateView | Add new bot |
| `/bots/<id>/edit/` | UpdateView | Edit bot |
| `/bots/<id>/delete/` | DeleteView | Remove bot |

*(Similar patterns for users, downloads, broadcasts, subscriptions)*

---

## Bot Commands

| Command | Handler | Description |
|---------|---------|-------------|
| `/start` | `start_command` | Welcome + main menu |
| `/help` | `help_command` | Usage instructions |
| `/stats` | `stats_command` | User's download stats |

---

## Installation Steps

### 1. Install Requirements
```bash
cd "C:\Users\Asus\Desktop\save bot"
pip install -r requirements.txt
```

### 2. Install FFmpeg
- **Windows:** Download from ffmpeg.org, extract to `C:\ffmpeg\`, add `C:\ffmpeg\bin` to PATH
- **Mac:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`

Verify: `ffmpeg -version`

### 3. Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Create Directories
```bash
mkdir media
mkdir media/downloads
```

### 5. Run the System

**Terminal 1 - Django:**
```bash
python manage.py runserver
# Visit: http://127.0.0.1:8000/admin
```

**Terminal 2 - Bot:**
```bash
python run_bot.py
# Or: python manage.py startbot
```

### 6. Configure Bot
1. Open http://127.0.0.1:8000/admin
2. Login with superuser
3. Go to **Bots** → **Add Bot**
4. Get token from @BotFather on Telegram
5. Enter username and token
6. Check **Active**
7. Save

Your bot is LIVE!

---

## File Cache System Deep Dive

### Problem
Without caching:
- User A requests video → Download from YouTube → Upload to Telegram → User gets video
- User B requests same video → Repeat entire process! Waste of bandwidth and time.

### Solution
```
1. When video is downloaded:
   - Save local file path: media/downloads/video_123.mp4
   - Upload to Telegram → Get file_id (e.g., "BAADBA...")
   - Save to database:
        url_hash: "a1b2c3..."
        file_id: "BAADBA..."
        file_path: "media/downloads/video_123.mp4"

2. When same URL requested again:
   - Calculate hash of URL (same as before)
   - Find CachedFile by hash
   - Check if file_path still exists
     → EXISTS: Resend file using file_id (instant, no upload!)
     → MISSING: Re-download and re-cache
```

### Benefits
- ⚡ Instant repeat downloads (Telegram API direct)
- 💾 Saves disk space (one copy)
- 🌐 Saves bandwidth (no re-upload)
- 💰 Reduces server costs

---

## Force-Subscribe Mechanism

### Why?
Prevent users from using bot without joining required channels (for promotions, compliance).

### How It Works
1. Admin adds channel in admin panel
2. Sets `is_required=True`
3. Bot checks membership when user sends `/start` or URL
4. If not member → Shows join buttons
5. User clicks "I've Subscribed"
6. Bot re-verifies via `get_chat_member()`
7. If verified → Grant access

### Implementation
```python
async def check_subscription(user_id, bot):
    required_channels = SubscriptionChannel.objects.filter(is_required=True)
    for channel in required_channels:
        member = await bot.get_chat_member(channel.channel_id, user_id)
        if member.status in ['left', 'kicked']:
            return False, [channel]
    return True, []
```

---

## Custom Template Tags

### `percentage(value, total)`
Returns `(value/total)*100` for progress bars.

**Usage:**
```django
<div style="width: {{ youtube_downloads|percentage:total_downloads }}%"></div>
```

### `filesizeformat(bytes)`
Formats file size: 1048576 → "1.0 MB"

**Usage:**
```django
{{ file_size|filesizeformat }}
```

---

## Template Hierarchy

```
base.html                  ← Base layout (sidebar, header, messages)
    ├── dashboard.html     ← Extends base, adds stats
    ├── bots/
    │   ├── list.html      ← Bot listing
    │   ├── form.html      ← Add/Edit form
    │   └── confirm_delete.html
    ├── users/
    │   ├── list.html      ← User list with filters
    │   ├── detail.html    ← User info + history
    │   └── confirm_delete.html
    ├── downloads/
    │   └── history.html   ← Download logs
    ├── broadcasts/
    │   ├── list.html      ← Broadcast list
    │   ├── form.html      ← Create/edit
    │   ├── send.html      ← Send confirmation
    │   └── confirm_delete.html
    └── subscriptions/
        ├── list.html      ← Channel list
        ├── form.html      ← Add/edit channel
        └── confirm_delete.html
```

All pages share:
- Sidebar navigation
- Bootstrap 5 styling
- Font Awesome icons
- Consistent header/footer

---

## API Integrations

### Telegram Bot API (via aiogram)
- **getChatMember:** Check subscription status
- **sendMessage:** Text responses
- **sendVideo:** Send downloaded videos
- **sendPhoto:** Send broadcast images

### yt-dlp
Extracts video info and downloads from:
- `youtube.com` / `youtu.be`
- `instagram.com`
- `tiktok.com`

**Options used:**
```python
{
    'format': 'best[filesize<50M]/best',
    'quiet': True,
    'noplaylist': True,
    'outtmpl': 'media/downloads/%(extractor)s_%(id)s.%(ext)s'
}
```

### ffmpeg
Converts videos to MP4 and extracts thumbnails:
```bash
ffmpeg -i input.mkv -c:v libx264 -c:a aac -movflags +faststart output.mp4
ffmpeg -i input.mp4 -ss 00:00:01 -vframes 1 -vf scale=320:-1 thumb.jpg
```

---

## Admin Dashboard Walkthrough

### Dashboard (`/`)
- Big number cards: Users, Downloads, Bots, Channels
- Progress bars: Platform distribution
- User stats: Active vs banned
- Recent downloads table

### Bots (`/bots/`)
- View all configured bots
- Add new bots
- Enable/disable bots
- Edit token/username
- Delete bots

### Users (`/users/`)
- See all Telegram users
- Filter by status (active/banned)
- Search by username/ID
- View user details + download history
- Ban/unban toggle

### Channels (`/subscriptions/`)
- List force-subscribe channels
- Add new channels (requires channel ID from @RawDataBot)
- Set required/optional
- Enable/disable channels

### Broadcasts (`/broadcasts/`)
- Create broadcast message
- Attach photo/video
- Schedule for later
- Send immediately
- Track progress (sent/failed)

### Downloads (`/downloads/history/`)
- View all download history
- Filter by platform
- Search by URL
- Download counts per platform

---

## Running Modes

### Development
```bash
python manage.py runserver
# Bot runs in separate terminal
python run_bot.py
```

### Production Considerations
Current system uses:
- SQLite (file-based, no server)
- Threading for broadcasts (not Celery)
- Polling for bot (use webhooks for production)

**To upgrade for production:**
1. Switch to PostgreSQL
2. Use gunicorn + nginx
3. Set up webhooks instead of polling
4. Use Celery + Redis for async tasks
5. Store files on S3/Cloudflare R2

---

## Security Notes

### Bot Token Security
✅ **Good:** Token stored in database, not hardcoded
⚠️ **Improve:** Use environment variables: `TELEGRAM_BOT_TOKEN=xxx`
❌ **Never:** Commit tokens to Git

### User Privacy
- Telegram IDs stored (not phone numbers)
- Usernames optional
- No personal data collected

### Admin Protection
- Django admin requires login
- Change default admin URL in production
- Enable 2FA on admin accounts

### Rate Limiting
- Currently no per-user limits
- Can add: `max_downloads_per_hour` field on BotUser

---

## Sample Data

### Example Bot User Record
```
telegram_id: 123456789
username: "john_doe"
first_name: "John"
last_name: "Doe"
is_banned: False
is_subscribed: True
download_count: 15
joined_at: 2026-01-15 10:30:00
last_activity: 2026-01-16 14:22:00
```

### Example Download
```
user: John Doe (123456)
platform: YOUTUBE
url: https://youtube.com/watch?v=abc123
file_path: media/downloads/youtube_20260116_142200_abc123.mp4
file_size: 15728640  (15 MB)
telegram_file_id: BAADBA...
downloaded_at: 2026-01-16 14:22:05
```

---

## Troubleshooting

### Bot doesn't respond
1. Check `run_bot.py` is running
2. Verify token in admin matches @BotFather
3. Ensure bot is marked Active
4. Check logs for errors

### Download fails
1. Verify ffmpeg in PATH: `ffmpeg -version`
2. URL must be from supported platforms
3. Video may be private/age-restricted
4. File > 50MB will be rejected

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Database locked (SQLite)
- Ensure only one process writing at a time
- For high concurrency, switch to PostgreSQL

---

## Extending the Platform

### Add New Platform
1. Update `detect_platform()` in `bots/bot.py`
2. Add platform to DownloadHistory.PLATFORM_CHOICES
3. yt-dlp handles most sites automatically!

### Add User Features
- Download quota system
- Preferred quality selection
- Download queue
- User registration

### Add Admin Features
- Export data to CSV
- Advanced analytics charts
- User messaging (1-on-1)
- Bulk user actions

### Integrate Payments
- Add `SubscriptionPlan` model
- Stripe/PayPal integration
- Premium features

---

## Deployment Checklist

### Before Going Live
- [ ] Change `SECRET_KEY` in settings.py
- [ ] Set `DEBUG = False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL
- [ ] Configure static files (collectstatic)
- [ ] Set up SSL certificate
- [ ] Use environment variables for secrets
- [ ] Add monitoring (Sentry/NewRelic)
- [ ] Setup daily backups
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Setup email (for admin alerts)

### Production Stack
```
VPS (Ubuntu 22.04)
├── nginx (reverse proxy + SSL)
├── gunicorn (WSGI server)
├── PostgreSQL (database)
├── Redis (future: Celery)
├── Telegram Bot (via webhook)
└── Cron jobs (cleanup old files)
```

---

## Performance Optimization

### Current State
- **Database:** SQLite (fine for <10k users)
- **Bot:** Single-threaded polling (fine for moderate usage)
- **Downloads:** Synchronous (blocks bot during download)
- **Storage:** Local disk

### Optimizations Available
1. **Async downloads:** Convert download to asyncio tasks
2. **Celery queue:** For heavy downloads
3. **Redis cache:** Faster than DB for file lookups
4. **CDN:** For serving cached videos
5. **Database:** PostgreSQL with connection pooling

---

## Contributing

This project is designed for learning. Feel free to:
- Add features
- Fix bugs
- Improve UI
- Write tests
- Add documentation

### Code Style
- PEP 8
- 4-space indentation
- Docstrings for functions
- Comments for complex logic

---

## License

MIT License - Free for personal and commercial use.

---

## Support

- Issues: Create GitHub issue
- Documentation: README.md, ARCHITECTURE.md, QUICKSTART.md
- Community: Telegram group (create one!)

---

**Built with Django, aiogram, yt-dlp, ffmpeg**

Happy downloading! 🚀
