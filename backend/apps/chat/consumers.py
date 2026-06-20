from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from apps.chat.models import ChatModel
from apps.listings.models import ListingModel


MAX_MESSAGE_LENGTH = 2000


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')

        if not self.user or self.user.is_anonymous:
            await self.close(code=4001)
            return

        self.listing_id = self.scope['url_route']['kwargs']['listing_id']
        self.room_name = f'listing_{self.listing_id}'

        if not await self.listing_exists(self.listing_id):
            await self.close(code=4004)
            return

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name,
        )
        await self.accept()

        await self.send_history()

    async def disconnect(self, close_code):
        room_name = getattr(self, 'room_name', None)

        if room_name:
            await self.channel_layer.group_discard(
                room_name,
                self.channel_name,
            )

    async def receive_json(self, content, **kwargs):
        action = content.get('action')

        if action != 'send_message':
            await self.send_json(
                {
                    'type': 'error',
                    'detail': 'Unsupported action.',
                }
            )
            return

        body = self.extract_message_body(content)

        if not body:
            await self.send_json(
                {
                    'type': 'error',
                    'detail': 'Message body is required.',
                }
            )
            return

        if len(body) > MAX_MESSAGE_LENGTH:
            await self.send_json(
                {
                    'type': 'error',
                    'detail': f'Message must not exceed {MAX_MESSAGE_LENGTH} characters.',
                }
            )
            return

        message = await self.save_message(body)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'message': message,
                'request_id': content.get('request_id'),
            },
        )

    async def chat_message(self, event):
        payload = {
            'type': 'message',
            'message': event['message'],
        }

        if event.get('request_id') is not None:
            payload['request_id'] = event['request_id']

        await self.send_json(payload)

    async def send_history(self):
        messages = await self.get_messages()

        await self.send_json(
            {
                'type': 'history',
                'messages': messages,
            }
        )

    @staticmethod
    def extract_message_body(content):
        data = content.get('data')

        if isinstance(data, dict):
            value = data.get('body') or data.get('message') or ''
        else:
            value = data or content.get('body') or content.get('message') or ''

        return str(value).strip()

    @database_sync_to_async
    def listing_exists(self, listing_id):
        return ListingModel.objects.filter(id=listing_id).exists()

    @database_sync_to_async
    def save_message(self, body):
        message = ChatModel.objects.create(
            body=body,
            user=self.user,
            listing_id=self.listing_id,
        )

        return self.serialize_message(message)

    @database_sync_to_async
    def get_messages(self):
        messages = (
            ChatModel.objects
            .select_related('user')
            .filter(listing_id=self.listing_id)
            .order_by('created_at')
        )

        return [
            self.serialize_message(message)
            for message in messages
        ]

    @staticmethod
    def serialize_message(message):
        return {
            'id': message.id,
            'body': message.body,
            'user': {
                'id': message.user_id,
                'username': message.user.username,
            },
            'listing_id': message.listing_id,
            'created_at': message.created_at.isoformat(),
        }