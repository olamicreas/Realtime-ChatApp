import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from .models import Messages
import logging

logger = logging.getLogger(__name__)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.recipient_username = self.scope['url_route']['kwargs']['username']
        self.recipient = await self.get_user(self.recipient_username)

        if self.recipient is None:
            await self.close()
        else:
            self.room_name = f"chat_{min(self.user.id, self.recipient.id)}_{max(self.user.id, self.recipient.id)}"
            self.room_group_name = f"chat_{self.room_name}"

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']

            # Save message to database
            await self.save_message(self.user, self.recipient, message)

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'sender': self.user.username
                }
            )

            # Send unread count notification
            unread_count = await self.get_unread_count(self.recipient, self.user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'unread_count',
                    'unread_count': unread_count,
                    'sender': self.user.username
                }
            )
        except Exception as e:
            logger.error(f"Error receiving message: {e}")

    async def chat_message(self, event):
        try:
            message = event['message']
            sender = event['sender']

            # Send message to WebSocket
            await self.send(text_data=json.dumps({
                'message': message,
                'sender': sender
            }))
        except Exception as e:
            logger.error(f"Error sending chat message: {e}")

    async def unread_count(self, event):
        try:
            unread_count = event['unread_count']
            sender = event['sender']

            # Send unread count notification to WebSocket
            await self.send(text_data=json.dumps({
                'unread_count': unread_count,
                'sender': sender
            }))
        except Exception as e:
            logger.error(f"Error sending unread count: {e}")

    @database_sync_to_async
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, sender, recipient, content):
        return Messages.objects.create(sender=sender, recipient=recipient, content=content, is_read=False)

    @database_sync_to_async
    def get_unread_count(self, recipient, sender):
        return Messages.objects.filter(recipient=recipient, sender=sender, is_read=False).count()