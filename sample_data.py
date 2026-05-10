"""
Django management command to create sample data for testing
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from bots.models import TelegramBot
from users.models import BotUser
from subscriptions.models import SubscriptionChannel
import random

class Command(BaseCommand):
    help = 'Creates sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Created superuser: admin / admin123'))

        # Create sample bots
        bots_data = [
            {'username': 'test_bot_1', 'token': '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11', 'is_active': True},
            {'username': 'my_downloader', 'token': '789012:XYZ-TEST5678mnOp-qrs89X3y2z456', 'is_active': False},
        ]

        for bot_data in bots_data:
            bot, created = TelegramBot.objects.get_or_create(
                username=bot_data['username'],
                defaults=bot_data
            )
            if created:
                self.stdout.write(f'✓ Created bot: @{bot.username}')

        # Create sample users
        names = ['Alice', 'Bob', 'Charlie', 'Diana', 'Eve']
        for i, name in enumerate(names, 1):
            user, created = BotUser.objects.get_or_create(
                telegram_id=1000000 + i,
                defaults={
                    'username': f'{name.lower()}_user',
                    'first_name': name,
                    'last_name': 'Doe' if i % 2 == 0 else '',
                    'is_banned': i == 5,  # Eve is banned
                    'is_subscribed': True,
                    'download_count': random.randint(1, 20),
                }
            )
            if created:
                self.stdout.write(f'✓ Created user: {user.first_name}')

        # Create sample subscription channel
        channel, created = SubscriptionChannel.objects.get_or_create(
            channel_id=-1001234567890,
            defaults={
                'channel_username': '@example_channel',
                'title': 'Example Channel',
                'invite_link': 'https://t.me/example_channel',
                'is_required': True,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'✓ Created channel: {channel.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created!'))
        self.stdout.write('\nYou can now:')
        self.stdout.write('1. python manage.py runserver')
        self.stdout.write('2. python run_bot.py')
        self.stdout.write('3. Visit http://127.0.0.1:8000/admin')
        self.stdout.write('   Login: admin / admin123')
