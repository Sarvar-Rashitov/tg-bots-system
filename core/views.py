from django.shortcuts import render
from django.db.models import Count, Sum, Q
from bots.models import TelegramBot
from users.models import BotUser
from downloads.models import DownloadHistory, CachedFile
from subscriptions.models import SubscriptionChannel
from broadcasts.models import BroadcastMessage

def dashboard(request):
    """Main analytics dashboard"""

    total_users = BotUser.objects.count()
    active_users = BotUser.objects.filter(is_banned=False).count()
    banned_users = BotUser.objects.filter(is_banned=True).count()
    subscribed_users = BotUser.objects.filter(is_subscribed=True).count()

    total_downloads = DownloadHistory.objects.count()
    youtube_downloads = DownloadHistory.objects.filter(platform='YOUTUBE').count()
    instagram_downloads = DownloadHistory.objects.filter(platform='INSTAGRAM').count()
    tiktok_downloads = DownloadHistory.objects.filter(platform='TIKTOK').count()

    # Determine most used platform
    platform_counts = {
        'YouTube': youtube_downloads,
        'Instagram': instagram_downloads,
        'TikTok': tiktok_downloads,
    }
    most_used_platform = max(platform_counts, key=platform_counts.get) if any(platform_counts.values()) else 'N/A'

    total_bots = TelegramBot.objects.count()
    active_bots = TelegramBot.objects.filter(is_active=True).count()

    total_channels = SubscriptionChannel.objects.count()
    required_channels = SubscriptionChannel.objects.filter(is_required=True, is_active=True).count()

    total_broadcasts = BroadcastMessage.objects.count()
    pending_broadcasts = BroadcastMessage.objects.filter(is_scheduled=True, scheduled_at__isnull=False).count()

    recent_users = BotUser.objects.order_by('-joined_at')[:10]
    recent_downloads = DownloadHistory.objects.order_by('-downloaded_at')[:10]

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'banned_users': banned_users,
        'subscribed_users': subscribed_users,
        'total_downloads': total_downloads,
        'youtube_downloads': youtube_downloads,
        'instagram_downloads': instagram_downloads,
        'tiktok_downloads': tiktok_downloads,
        'most_used_platform': most_used_platform,
        'total_bots': total_bots,
        'active_bots': active_bots,
        'total_channels': total_channels,
        'required_channels': required_channels,
        'total_broadcasts': total_broadcasts,
        'pending_broadcasts': pending_broadcasts,
        'recent_users': recent_users,
        'recent_downloads': recent_downloads,
    }

    return render(request, 'dashboard.html', context)
