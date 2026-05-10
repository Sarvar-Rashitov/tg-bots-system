"""Broadcasts app views"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import BroadcastMessage
from users.models import BotUser
import logging
import asyncio
import threading
from aiogram.types import FSInputFile

logger = logging.getLogger(__name__)

def send_broadcast_async(broadcast_id: int):
    """
    Send broadcast in background thread using asyncio
    """
    def run():
        try:
            # Need Django setup for this thread
            import os
            import django
            os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'telegram_downloader.settings')
            django.setup()

            from broadcasts.models import BroadcastMessage
            from users.models import BotUser
            from bots.models import TelegramBot
            from aiogram import Bot
            from aiogram.types import FSInputFile
            from asgiref.sync import sync_to_async
            import asyncio

            @sync_to_async
            def get_broadcast():
                return BroadcastMessage.objects.get(id=broadcast_id)

            @sync_to_async
            def get_users():
                return list(BotUser.objects.filter(is_banned=False))

            @sync_to_async
            def get_bot_token():
                bot_instance = TelegramBot.objects.filter(is_active=True).first()
                return bot_instance.token if bot_instance else None

            @sync_to_async
            def update_broadcast_status(broadcast, is_sent=None, sent_count=None, failed_count=None):
                if is_sent is not None:
                    broadcast.is_sent = is_sent
                if sent_count is not None:
                    broadcast.sent_count = sent_count
                if failed_count is not None:
                    broadcast.failed_count = failed_count
                broadcast.save()

            async def send_messages():
                try:
                    # Get broadcast and users
                    broadcast = await get_broadcast()
                    users = await get_users()

                    # Mark as sending
                    await update_broadcast_status(broadcast, is_sent=False)

                    # Get bot token
                    token = await get_bot_token()
                    if not token:
                        logger.error("No active bot found")
                        return

                    bot = Bot(token=token)
                    sent = 0
                    failed = 0

                    logger.info(f"Starting broadcast to {len(users)} users")

                    for user in users:
                        try:
                            if broadcast.message_type == 'TEXT':
                                await bot.send_message(
                                    chat_id=user.telegram_id,
                                    text=broadcast.message,
                                    parse_mode='HTML'
                                )
                            elif broadcast.message_type == 'PHOTO' and broadcast.media_file:
                                await bot.send_photo(
                                    chat_id=user.telegram_id,
                                    photo=FSInputFile(broadcast.media_file.path),
                                    caption=broadcast.message or ""
                                )
                            elif broadcast.message_type == 'VIDEO' and broadcast.media_file:
                                await bot.send_video(
                                    chat_id=user.telegram_id,
                                    video=FSInputFile(broadcast.media_file.path),
                                    caption=broadcast.message or ""
                                )

                            sent += 1
                            logger.info(f"Sent to user {user.telegram_id}")
                        except Exception as e:
                            logger.error(f"Failed to send to {user.telegram_id}: {e}")
                            failed += 1

                        # Update progress every 5 messages
                        if (sent + failed) % 5 == 0:
                            await update_broadcast_status(broadcast, sent_count=sent, failed_count=failed)

                        # Small delay to avoid rate limits
                        await asyncio.sleep(0.1)

                    # Final update
                    await update_broadcast_status(broadcast, is_sent=True, sent_count=sent, failed_count=failed)
                    
                    # Close bot session
                    await bot.session.close()
                    
                    logger.info(f"Broadcast completed: {sent} sent, {failed} failed")

                except Exception as e:
                    logger.error(f"Broadcast send error: {e}")

            asyncio.run(send_messages())

        except Exception as e:
            logger.error(f"Broadcast error: {e}")

    # Run in separate thread
    thread = threading.Thread(target=run, daemon=True)
    thread.start()


class BroadcastListView(LoginRequiredMixin, ListView):
    model = BroadcastMessage
    template_name = 'broadcasts/list.html'
    context_object_name = 'broadcasts'
    paginate_by = 20

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')


class BroadcastCreateView(LoginRequiredMixin, CreateView):
    model = BroadcastMessage
    template_name = 'broadcasts/form.html'
    fields = ['title', 'message', 'message_type', 'media_file', 'is_scheduled', 'scheduled_at']
    success_url = reverse_lazy('broadcasts:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.total_users = BotUser.objects.filter(is_banned=False).count()
        messages.success(self.request, 'Broadcast created!')

        response = super().form_valid(form)

        # Start sending if not scheduled
        if not form.instance.is_scheduled:
            send_broadcast_async(form.instance.id)

        return response


class BroadcastUpdateView(LoginRequiredMixin, UpdateView):
    model = BroadcastMessage
    template_name = 'broadcasts/form.html'
    fields = ['title', 'message', 'message_type', 'media_file', 'is_scheduled', 'scheduled_at']
    success_url = reverse_lazy('broadcasts:list')

    def form_valid(self, form):
        messages.success(self.request, 'Broadcast updated!')
        return super().form_valid(form)


class BroadcastDeleteView(LoginRequiredMixin, DeleteView):
    model = BroadcastMessage
    template_name = 'broadcasts/confirm_delete.html'
    success_url = reverse_lazy('broadcasts:list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Broadcast deleted!')
        return super().delete(request, *args, **kwargs)


class BroadcastSendView(LoginRequiredMixin, DetailView):
    model = BroadcastMessage
    template_name = 'broadcasts/send.html'
    context_object_name = 'broadcast'

    def post(self, request, *args, **kwargs):
        broadcast = self.get_object()
        send_broadcast_async(broadcast.id)
        messages.success(request, 'Broadcast is being sent!')
        return redirect('broadcasts:list')
