"""
Django management command to start Telegram bots
Usage: python manage.py startbot
"""

import asyncio
import logging
from django.core.management.base import BaseCommand
from bots.bot import main as bot_main

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Starts the Telegram downloader bot(s)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Telegram Downloader Bot...'))
        try:
            asyncio.run(bot_main())
        except KeyboardInterrupt:
            self.stdout.write(self.style.SUCCESS('Bot stopped by user'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
            logger.error(f'Bot error: {e}', exc_info=True)
