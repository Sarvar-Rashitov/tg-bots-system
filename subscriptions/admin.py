from django.contrib import admin
from .models import SubscriptionChannel

@admin.register(SubscriptionChannel)
class SubscriptionChannelAdmin(admin.ModelAdmin):
    list_display = ('channel_id', 'channel_username', 'title', 'is_required', 'is_active', 'added_at')
    list_filter = ('is_required', 'is_active', 'added_at')
    search_fields = ('channel_username', 'title')
    list_editable = ('is_required', 'is_active')
    readonly_fields = ('channel_id', 'added_at')
    fieldsets = (
        ('Channel Info', {
            'fields': ('channel_id', 'channel_username', 'title')
        }),
        ('Settings', {
            'fields': ('invite_link', 'is_required', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('added_at',),
            'classes': ('collapse',)
        }),
    )
