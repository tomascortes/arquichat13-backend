from django.contrib import admin

from .models import ChatRoom


admin.site.register(
    ChatRoom,
    list_display=["id", "topic"],
    list_display_links=["id", "topic"],
)

