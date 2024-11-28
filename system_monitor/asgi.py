"""
ASGI config for system_monitor project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'system_monitor.settings')

application = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import get_channel_layer
from django.urls import path
from monitor.consumers import StatsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_name.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        path('ws/stats/', StatsConsumer.as_asgi()),
    ]),
})

