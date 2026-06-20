import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'configs.settings')

django_asgi_app = get_asgi_application()

from configs.routing import websocket_urlpatterns
from core.middlewares.auth_socket_middleware import AuthSocketMiddleware


application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': AuthSocketMiddleware(
            URLRouter(websocket_urlpatterns),
        ),
    }
)