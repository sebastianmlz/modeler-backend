"""
ASGI config for backend project.

Permite HTTP y WebSocket (Channels).
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Importa el routing de colaboración si existe, si no, usa un placeholder
try:
	import Apps.collaboration.routing
	websocket_urlpatterns = Apps.collaboration.routing.websocket_urlpatterns
except ImportError:
	websocket_urlpatterns = []

application = ProtocolTypeRouter({
	"http": get_asgi_application(),
	"websocket": AuthMiddlewareStack(
		URLRouter(
			websocket_urlpatterns
		)
	),
})
