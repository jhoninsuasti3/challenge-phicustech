# routing.py

from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import GameConsumer

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/partida/<int:partida_id>/", MyConsumer.as_asgi()),
    ]),
})
