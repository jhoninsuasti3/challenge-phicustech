# tictactoe_game/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.partida_id = self.scope['url_route']['kwargs']['partida_id']
        self.partida_group_name = f"partida_{self.partida_id}"

        await self.channel_layer.group_add(
            self.partida_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.partida_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        movimiento = data['movimiento']

        await self.channel_layer.group_send(
            self.partida_group_name,
            {
                'type': 'movimiento',
                'movimiento': movimiento
            }
        )

    async def movimiento(self, event):
        movimiento = event['movimiento']
        await self.send(text_data=json.dumps({
            'movimiento': movimiento
        }))
