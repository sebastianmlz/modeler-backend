import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DiagramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.diagram_id = self.scope['url_route']['kwargs']['diagram_id']
        self.room_group_name = f'diagram_{self.diagram_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'diagram_event',
                'message': text_data,
            }
        )

    async def diagram_event(self, event):
        await self.send(text_data=event['message'])