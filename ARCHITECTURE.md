# Architecture Documentation

## System Overview

This is a **Django MVT** (Model-View-Template) based Telegram downloader bot management platform. It provides a centralized dashboard to manage multiple Telegram bots, monitor downloads, manage users, and send broadcasts.

## Design Principles

- **Simplicity**: Clean, beginner-friendly code
- **Modularity**: Each app handles one responsibility
- **Beginner-Friendly**: Easy to understand and extend
- **Production-Ready Foundation**: Can be scaled with proper infrastructure

## Architecture Diagram

```
┌─────────────────┐
│   Django Admin  │ ← Management Dashboard
│   (Web UI)      │
└────────┬────────┘
         │
         ├──> Models (SQLite Database)
         │    ├── TelegramBot
         │    ├── BotUser
         │    ├── DownloadHistory
         │    ├── CachedFile
         │    ├── SubscriptionChannel
         │    └── BroadcastMessage
         │
         └──> Bot Service (run_bot.py / startbot)
              ├── aiogram 3 (Telegram API)
              ├── yt-dlp (Video Download)
              ├── ffmpeg (Video Processing)
              └── Cache System
                   │
                   └──> Telegram Users
```

## App Structure

### 1. core (Dashboard & Analytics)

**Purpose**: Main dashboard and analytics

**Models**: None (uses models from other apps)

**Views**:
- `dashboard` - Main analytics view with statistics

**Templates**:
- `dashboard.html` - Main dashboard with charts and stats

### 2. bots (Bot Management)

**Purpose**: Manage Telegram bot instances

**Models**:
- `TelegramBot` - Stores bot token, username, active status

**Views**:
- `BotListView` - List all bots
- `BotCreateView` - Add new bot
- `BotUpdateView` - Edit bot settings
- `BotDeleteView` - Remove bot

**Features**:
- Add multiple bots (each with different tokens)
- Enable/disable bots
- View bot statistics

### 3. users (User Management)

**Purpose**: Track and manage Telegram users

**Models**:
- `BotUser` - Telegram user data, ban status, stats

**Views**:
- `UserListView` - List users with filters
- `UserDetailView` - View user details & history
- Toggle ban/unban

**Features**:
- View all users
- Ban/unban users
- See download history per user
- Track user activity

### 4. downloads (Download System)

**Purpose**: Handle video downloads and caching

**Models**:
- `DownloadHistory` - Log of all downloads
- `CachedFile` - Cache by URL hash

**Services**:
- `VideoDownloader` (downloads/downloader.py)
  - Detects platform (YouTube/Instagram/TikTok)
  - Downloads using yt-dlp
  - Converts to MP4 using ffmpeg
  - Extracts thumbnails

**Views**:
- `DownloadHistoryListView` - All downloads with filters

**Features**:
- Platform detection
- File size validation
- Thumbnail extraction
- Progress tracking

### 5. subscriptions (Force-Subscribe)

**Purpose**: Require users to join channels

**Models**:
- `SubscriptionChannel` - Channel config (ID, username, required flag)

**Views**:
- `ChannelListView` - List channels
- `ChannelCreateView` - Add channel
- `ChannelUpdateView` - Edit channel
- `ChannelDeleteView` - Remove channel

**Features**:
- Multiple channels support
- Required vs optional channels
- Active/inactive toggle

### 6. broadcasts (Messaging)

**Purpose**: Send messages to all users

**Models**:
- `BroadcastMessage` - Message content, type, scheduling

**Views**:
- `BroadcastListView` - All broadcasts
- `BroadcastCreateView` - Create broadcast
- `BroadcastSendView` - Execute broadcast

**Features**:
- Text, photo, video broadcasts
- Simple scheduling (send immediately or schedule)
- Progress tracking (sent count)

## Database Schema

```sql
-- Telegram Bot Instance
telegram_bot
├── id (PK)
├── bot_owner (FK -> User)
├── token (unique)
├── username
├── is_active (boolean)
├── created_at
└── updated_at

-- Telegram Users
bot_user
├── id (PK)
├── telegram_id (unique, bigint)
├── username
├── first_name
├── last_name
├── is_banned (boolean)
├── is_subscribed (boolean)
├── download_count
├── joined_at
└── last_activity

-- Download Logs
download_history
├── id (PK)
├── user (FK -> BotUser)
├── platform (YOUTUBE/INSTAGRAM/TIKTOK)
├── url
├── file_path
├── file_size
├── downloaded_at
└── telegram_file_id

-- File Cache
cached_file
├── id (PK)
├── url_hash (unique, SHA256)
├── original_url
├── file_id (Telegram file_id)
├── file_path
├── file_size
├── download_count
├── created_at
└── last_used

-- Force-Subscribe Channels
subscription_channel
├── id (PK)
├── channel_id (unique, Telegram ID)
├── channel_username (unique)
├── title
├── invite_link
├── is_required (boolean)
├── is_active (boolean)
└── added_at

-- Broadcast Messages
broadcast_message
├── id (PK)
├── title
├── message
├── message_type (TEXT/PHOTO/VIDEO)
├── media_file
├── total_users
├── sent_count
├── failed_count
├── is_scheduled
├── scheduled_at
├── created_at
└── created_by (FK -> User)
```

## Bot Workflow

1. **User sends /start**
   - Bot checks if user exists in DB (creates if new)
   - Checks subscription to required channels
   - If not subscribed → show subscription keyboard
   - If subscribed → show main menu

2. **User sends URL**
   - Bot detects platform
   - Checks cache for this URL hash
   - If cached → send from Telegram file_id (instant)
   - If not cached → download with yt-dlp
   - Convert with ffmpeg if needed
   - Upload to Telegram
   - Save to DB (history + cache)

3. **Broadcast Sent**
   - Admin creates broadcast message
   - Clicks "Send"
   - Background thread retrieves all active users
   - Sends message via bot API (with delay to avoid rate limits)
   - Updates progress

## File Cache System

The cache uses URL SHA256 hash as key:

```python
url_hash = hashlib.sha256(url.encode()).hexdigest()
```

When downloading:
1. Calculate hash
2. Query `CachedFile` by hash
3. If exists → use `telegram_file_id` to resend
4. If not → download, upload, store file_id

Benefits:
- No duplicate downloads
- No duplicate uploads to Telegram
- Instant repeat downloads
- Saves bandwidth

## Force Subscribe Flow

```
User sends /start
    ↓
Bot checks SubscriptionChannel.objects.filter(is_required=True)
    ↓
If none → proceed
    ↓
For each required channel:
    - Check Telegram API membership
    ↓
If any missing:
    - Show inline keyboard with join links
    - Show "I've Subscribed" button
    ↓
User joins channels & clicks button
    ↓
Bot re-checks membership
    ↓
Verified → show main menu
```

## Scaling Considerations

This is a starter architecture. For production:

### Database
- Switch from SQLite to PostgreSQL
- Add indexes on frequently queried fields
- Consider partitioning download_history

### Bot Service
- Use webhooks instead of polling (lower latency)
- Implement retry logic for failed downloads
- Add download queue with Redis/Celery

### Media Storage
- Replace local filesystem with S3/Cloud Storage
- CDN for faster delivery

### Monitoring
- Add Sentry for error tracking
- Prometheus metrics
- Admin notifications for failures

### Security
- Rate limiting per user
- IP blocking
- Content filtering

## Security Best Practices

1. **Never expose bot tokens** - Store in environment variables
2. **Use HTTPS** in production
3. **Restrict admin access** - Only trusted staff
4. **Validate URLs** - Prevent SSRF attacks
5. **File size limits** - Prevent DoS
6. **Regular backups** - Database and media

## Code Style

- PEP 8 compliant
- Type hints where possible
- Docstrings for complex functions
- Clean separation of concerns
- DRY principle

## Testing

To write tests:
```bash
# Create tests.py in each app
# Use Django's test framework
python manage.py test
```

## Deployment Checklist

- [ ] Install system dependencies (ffmpeg)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use environment variables for secrets
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Setup database (PostgreSQL)
- [ ] Setup gunicorn/uWSGI
- [ ] Setup nginx reverse proxy
- [ ] Configure SSL certificates
- [ ] Setup process manager (systemd/supervisor)
- [ ] Enable logging
- [ ] Setup monitoring
- [ ] Backup strategy

## Maintenance

### Daily
- Monitor broadcasts
- Check for failed downloads
- Review user reports

### Weekly
- Clean old files from media/downloads
- Review analytics
- Check storage usage

### Monthly
- Database optimization
- Security updates
- Review bot performance

---

This architecture is designed to be **simple yet scalable**. Start with SQLite and polling, upgrade to PostgreSQL and webhooks as you grow.
