import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import ChatMessage
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):

        self.other_user_id = self.scope["url_route"]["kwargs"]["user_id"]

        self.current_user = self.scope["user"]

        if self.current_user.is_anonymous:
            await self.close()
            return

        user_ids = sorted([
            self.current_user.id,
            int(self.other_user_id)
        ])

        self.room_group_name = (
            f"chat_{user_ids[0]}_{user_ids[1]}"
        )

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        data = json.loads(text_data)

        message = data.get("message", "").strip()

        if not message:
            return

        receiver = await self.get_user(
            int(self.other_user_id)
        )

        chat_message = await self.save_message(
            self.current_user,
            receiver,
            message
        )

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": chat_message.message,
                "sender": chat_message.sender.username,
                "sender_id": chat_message.sender.id,
                "created_at": chat_message.created_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            }
        )

    async def chat_message(self, event):

        await self.send(
            text_data=json.dumps({
                "message": event["message"],
                "sender": event["sender"],
                "sender_id": event["sender_id"],
                "created_at": event["created_at"],
            })
        )

    @database_sync_to_async
    def get_user(self, user_id):

        return User.objects.get(id=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, message):

        return ChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message=message
        )