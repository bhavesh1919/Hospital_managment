from django.contrib import admin
from .models import ChatMessage
# Register your models here.
@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "receiver",
        "message",
        "created_at",
        "is_read",
    )

    list_filter = (
        "is_read",
        "created_at",
    )

    search_fields = (
        "sender__username",
        "receiver__username",
        "message",
    )