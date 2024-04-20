import os

 
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.sessions import SessionMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator,OriginValidator
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")


from chat.routing import websocket_urlpatterns # type: ignore
application =ProtocolTypeRouter({
    "http":   get_asgi_application(),
     "websocket":  OriginValidator(
            AuthMiddlewareStack(
                SessionMiddlewareStack(URLRouter(websocket_urlpatterns))
            ),
            ["*"]
        ),
})