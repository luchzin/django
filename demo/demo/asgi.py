import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
django.setup()



from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from chat.routing import websocket_urlpatterns  # type: ignore
from channels.sessions import SessionMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

application = ProtocolTypeRouter({
    "http":   get_asgi_application(),
    "websocket":  OriginValidator(
        AuthMiddlewareStack(
            SessionMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
        ["*"]
    ),
})
