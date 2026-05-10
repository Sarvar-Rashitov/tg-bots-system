# Quick Start Guide

Get your Telegram downloader bot running in 5 minutes!

## Step 1: Install Dependencies

```bash
cd "C:\Users\Asus\Desktop\save bot"
pip install -r requirements.txt
```

## Step 2: Install FFmpeg

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg\`
3. Add `C:\ffmpeg\bin` to System PATH
4. Restart terminal and run: `ffmpeg -version`

**Linux/Mac:**
```bash
sudo apt install ffmpeg      # Ubuntu/Debian
brew install ffmpeg          # Mac
```

## Step 3: Setup Django

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Step 4: Start the Bot

Open a new terminal window and run:
```bash
cd "C:\Users\Asus\Desktop\save bot"
python run_bot.py
```

## Step 5: Start Django Server

```bash
python manage.py runserver
```

## Step 6: Configure Your Bot

1. Go to http://127.0.0.1:8000/admin
2. Login with superuser credentials
3. Click **Bots** → **Add Bot**
4. Get token from @BotFather on Telegram
5. Enter bot username and token
6. Check **Active** and save

Your bot is now live!

## Step 7: Add Force-Subscribe Channel (Optional)

1. In admin, click **Channels** → **Add Channel**
2. Get channel ID from @RawDataBot
3. Enter channel details and mark as **Required**
4. Users will need to subscribe before using bot

## Test Your Bot

1. Open Telegram
2. Search for your bot
3. Send `/start`
4. Send a YouTube/Instagram/TikTok link
5. Watch it download!

## Common Issues

### "ModuleNotFoundError: No module named 'yt_dlp'"
```bash
pip install -r requirements.txt
```

### "FFmpeg not found"
Make sure ffmpeg is in PATH. Test: `ffmpeg -version`

### Bot doesn't respond
- Check token is correct
- Ensure bot is marked active in admin
- Make sure `run_bot.py` is running

### Download fails
- URL must be from YouTube, Instagram, or TikTok
- Video must be public
- File size must be under 50MB

## Next Steps

- Add more bots (each with different tokens)
- Configure force-subscribe channels
- Create broadcast announcements
- Monitor analytics on dashboard

Enjoy your Telegram downloader platform!
