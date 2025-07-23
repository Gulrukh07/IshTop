import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User

from chat.models import Chat


class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        receiver = self.scope['url_route']['kwargs']['receiver']
        sender = self.scope['url_route']['kwargs']['sender']
        self.room_name = '_'.join(sorted([str(receiver), str(sender)], key=int))
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
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
        message = data['message']
        sender_id = self.scope['url_route']['kwargs']['sender']
        receiver_id = self.scope['url_route']['kwargs']['receiver']

        # Save message to database
        sender = await sync_to_async(User.objects.get)(id=sender_id)
        receiver = await sync_to_async(User.objects.get)(id=receiver_id)
        await sync_to_async(Chat.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id
        }))
