# Пример routing.py для приложения
from django.urls import re_path
from .consumers import NotificationConsumer #ChatConsumer
#
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    #re_path(r'ws/chat/$', ChatConsumer.as_asgi()),

    #re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),#
    re_path(r'ws/chat/notifications/$', NotificationConsumer.as_asgi()),#
]
#
application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})