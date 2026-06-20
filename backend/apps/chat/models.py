from django.conf import settings
from django.db import models

from core.models import BaseModel
from apps.listings.models import ListingModel


class ChatModel(BaseModel):
    body = models.TextField(max_length=2000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages',
    )
    listing = models.ForeignKey(
        ListingModel,
        on_delete=models.CASCADE,
        related_name='chat_messages',
    )

    class Meta:
        db_table = 'chat'
        ordering = ('created_at',)
        indexes = [
            models.Index(fields=('listing', 'created_at')),
            models.Index(fields=('user', 'created_at')),
        ]

    def __str__(self):
        return f'Message #{self.pk} for listing #{self.listing_id}'