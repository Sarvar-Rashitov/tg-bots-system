from django.contrib import admin
from .models import BotUser
from downloads.models import DownloadHistory

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'username', 'first_name', 'last_name', 'is_banned', 'is_subscribed', 'download_count', 'joined_at', 'last_activity')
    list_filter = ('is_banned', 'is_subscribed', 'joined_at')
    search_fields = ('telegram_id', 'username', 'first_name', 'last_name')
    list_editable = ('is_banned', 'is_subscribed')
    readonly_fields = ('telegram_id', 'joined_at', 'last_activity', 'download_count')
    fieldsets = (
        ('User Info', {
            'fields': ('telegram_id', 'username', 'first_name', 'last_name')
        }),
        ('Status', {
            'fields': ('is_banned', 'is_subscribed', 'download_count')
        }),
        ('Activity', {
            'fields': ('joined_at', 'last_activity'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform', 'url', 'file_size_display', 'downloaded_at')
    list_filter = ('platform', 'downloaded_at')
    search_fields = ('url', 'user__username', 'user__telegram_id')
    readonly_fields = ('downloaded_at',)
    fieldsets = (
        ('Download Info', {
            'fields': ('user', 'platform', 'url', 'file_size')
        }),
        ('File Details', {
            'fields': ('file_path', 'telegram_file_id'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('downloaded_at',),
            'classes': ('collapse',)
        }),
    )

    def file_size_display(self, obj):
        if obj.file_size:
            size_mb = obj.file_size / (1024 * 1024)
            return f"{size_mb:.2f} MB"
        return "0 MB"
    file_size_display.short_description = 'File Size'
