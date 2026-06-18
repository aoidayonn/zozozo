from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/tetris/(?P<room_name>\w+)/$", consumers.TetrisConsumer.as_asgi()),
]