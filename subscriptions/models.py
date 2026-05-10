from django.db import models


class SubscriptionChannel(models.Model):
    channel_id = models.BigIntegerField(unique=True)
    channel_username = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    invite_link = models.CharField(max_length=500, blank=True)
    is_required = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Subscription Channel'
        verbose_name_plural = 'Subscription Channels'
        ordering = ['title']

    def __str__(self):
        return self.title