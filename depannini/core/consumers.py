# your_app/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class AssistanceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get assistance_id from URL route
        self.assistance_id = self.scope['url_route']['kwargs']['assistance_id']
        self.room_group_name = f"assistance_{self.assistance_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        print('connection established')
        await self.accept()

        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected to channel_{self.assistance_id}'
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            user_id = data.get('user_id')
            lat = data.get('lat')
            lng = data.get('lng')

            if lat is not None and lng is not None and user_id is not None:
                from django.contrib.auth import get_user_model
                from asgiref.sync import sync_to_async
                User = get_user_model()

                @sync_to_async
                def update_user_location():
                    print('saving to database ..')
                    try:
                        user = User.objects.get(id=user_id)
                        print(f'user {user} found')
                        user.current_lat = lat
                        user.current_lng = lng
                        user.save()
                        return True
                    except:
                        return False

                success = await update_user_location()

                if success:
                    # Still broadcast the location update to the room group
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'location_update',
                            'lat': lat,
                            'lng': lng,
                            'user_id': user_id
                        }
                    )
                else:
                    await self.send(text_data=json.dumps({
                        'type': 'error',
                        'message': f'User with ID {user_id} not found'
                    }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'Not valid data'
                }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': str(e)
            }))

    # Handler for chat messages
    async def chat_message(self, event):
        # Send chat messages to client
        await self.send(text_data=json.dumps({
            'type': 'chat',
            'message': event['message'],
            'sender': event['sender']
        }))

    # Handler for custom group messages
    async def assistance_update(self, event):
        # Send status updates to client
        await self.send(text_data=json.dumps({
            'type': 'status',
            'status': event['status'],
            'assistant': event.get('assistant'),
            'client': event.get('client')
        }))

    async def location_update(self, event):
        # Send location updates to client
        await self.send(text_data=json.dumps({
            'type': 'location',
            'lat': event['lat'],
            'lng': event['lng'],
            'user_id': event['user_id']
        }))


class AssistantConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.assistant_id = self.scope['url_route']['kwargs']['assistant_id']
        self.room_group_name = f"assistant_{self.assistant_id}"

        print(
            f'assistant {self.assistant_id} connected to channel {self.room_group_name}')

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Notify that connection was successful
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected as assistant_{self.assistant_id}'
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (not used here but required)
    async def receive(self, text_data):
        await self.send(text_data=json.dumps({"message": "Echo: " + text_data}))

    async def new_request(self, event):
        # Send request to assistant
        print(f'sending request to {self.assistant_id}')
        await self.send(text_data=json.dumps({
            'type': 'new_assistance_request',
            'assistance_id': event['assistance_id'],
            'pickup_location': event['pickup_location'],
            'client': event.get('client')
        }))
