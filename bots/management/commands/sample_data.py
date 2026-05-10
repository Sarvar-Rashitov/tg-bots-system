"""
Management command to create sample data
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

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('✓ Created superuser: admin / admin123'))

        # Create sample bot
        bot, created = TelegramBot.objects.get_or_create(
            username='my_test_bot',
            defaults={
                'token': '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11',
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'✓ Created bot: @{bot.username}')

        # Create sample users
        for i in range(1, 6):
            user, created = BotUser.objects.get_or_create(
                telegram_id=100000 + i,
                defaults={
                    'username': f'user_{i}',
                    'first_name': f'User{i}',
                    'is_banned': i == 5,
                    'is_subscribed': True,
                    'download_count': random.randint(0, 15),
                }
            )
            if created:
                self.stdout.write(f'✓ Created user: {user.first_name}')

        # Create sample channel
        channel, created = SubscriptionChannel.objects.get_or_create(
            channel_id=-100123456789,
            defaults={
                'channel_username': '@demo_channel',
                'title': 'Demo Channel',
                'is_required': True,
                'is_active': True,
            }
        )
        if created:
            self.stdout.write(f'✓ Created channel: {channel.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Sample data created!'))
        self.stdout.write('Start server: python manage.py runserver')
        self.stdout.write('Start bot: python run_bot.py')
