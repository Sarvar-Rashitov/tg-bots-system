from django.db import models


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    username = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=5, default='en', choices=[
        ('en', 'English'),
        ('ru', 'Русский'),
        ('uz', "O'zbek")
    ])
    last_url = models.URLField(blank=True, null=True)  # Oxirgi yuborilgan URL
    is_banned = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    download_count = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural = 'Bot Users'
        ordering = ['-joined_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name