from django.contrib import admin
from .models import BroadcastMessage

@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'message_type', 'sent_count', 'total_users', 'created_at', 'scheduled_at', 'is_sent')
    list_filter = ('message_type', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('sent_count', 'failed_count', 'created_at')
    fieldsets = (
        ('Content', {
            'fields': ('title', 'message', 'message_type', 'media_file')
        }),
        ('Target', {
            'fields': ('total_users',)
        }),
        ('Scheduling', {
            'fields': ('is_scheduled', 'scheduled_at'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('sent_count', 'failed_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_sent(self, obj):
        return obj.sent_count >= obj.total_users
    is_sent.boolean = True
    is_sent.short_description = 'Completed'
