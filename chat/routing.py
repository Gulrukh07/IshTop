# chat/routing.py
from django.urls import re_path
from .consumers import  PrivateChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/private_chat/(?P<sender>\d+)/(?P<receiver>\d+)/?$', PrivateChatConsumer.as_asgi()),

]