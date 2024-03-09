"""
ASGI config for social network project.

It exposes the ASGI callable as a module-level variable named ``application``.

"""
import os
import sys
import django
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from app.consumers import DirectChatConsumer

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')

django.setup()

http_application = get_asgi_application()
websocket_application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            path('ws/<int:id>', DirectChatConsumer.as_asgi())
        ])
    )
})

application = ProtocolTypeRouter({
    "http": http_application,
    "websocket": websocket_application
})
