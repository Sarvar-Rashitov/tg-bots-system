from django.db import models
from django.contrib.auth.models import User


class BroadcastMessage(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('TEXT', 'Text'),
        ('PHOTO', 'Photo'),
        ('VIDEO', 'Video'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPE_CHOICES, default='TEXT')
    media_file = models.FileField(upload_to='broadcast_media/', null=True, blank=True)
    total_users = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    is_sent = models.BooleanField(default=False)
    is_scheduled = models.BooleanField(default=False)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='broadcasts',
        null=True
    )

    class Meta:
        verbose_name = 'Broadcast Message'
        verbose_name_plural = 'Broadcast Messages'
        ordering = ['-created_at']

    def __str__(self):
        return self.title