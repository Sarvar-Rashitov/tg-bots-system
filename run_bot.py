"""
Bot runner script - runs all active Telegram bots
"""

import asyncio
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')
django.setup()

from bots.bot import main

if __name__ == '__main__':
    print("Starting Telegram Downloader Bot Service...")
    print("Press Ctrl+C to stop\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
