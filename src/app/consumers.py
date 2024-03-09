import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import WebsocketConsumer
from .models import DmChat
from channels.db import database_sync_to_async
from django.contrib.auth.models import User


class DirectChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = f"user_{self.user.id}"
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        json_data = json.loads(text_data)
        # print(json_data)
        message = json_data['message']
        sent_to_id = json_data['sent_to']
        r_name = f"user_{sent_to_id}"
        room_name = f'chat_{r_name}'

        await self.save_message(message, sent_to_id)
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self, message, sent_to_id):
        sent_to = User.objects.get(id=sent_to_id)
        DmChat.objects.create(
            content=message,
            sent_by=self.scope['user'],
            sent_to=sent_to,
            chat_name=self.room_group_name
        )

