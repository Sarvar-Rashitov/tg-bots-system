from django.db import models
from django.contrib.auth.models import User


class TelegramBot(models.Model):
    bot_owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='telegram_bots',
        null=True,
        blank=True
    )
    token = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Telegram Bot'
        verbose_name_plural = 'Telegram Bots'

    def __str__(self):
        return f"@{self.username}"