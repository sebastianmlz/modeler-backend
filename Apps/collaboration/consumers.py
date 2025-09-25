import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from Apps.modeling.models import Diagram
from Apps.workspace.models import ProjectMember
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class DiagramConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.diagram_id = self.scope['url_route']['kwargs']['diagram_id']

        # --- AUTENTICACIÓN JWT MANUAL ---
        # Extraer token de la query string
        token = None
        query_string = self.scope.get('query_string', b'').decode()
        for part in query_string.split('&'):
            if part.startswith('token='):
                token = part.split('=', 1)[1]
                break

        self.user = None
        if token:
            try:
                validated_token = AccessToken(token)
                user_id = validated_token['user_id']
                User = get_user_model()
                self.user = await database_sync_to_async(User.objects.get)(id=user_id)
            except Exception:
                self.user = None
        else:
            # Si no hay token, usar usuario de sesión (por si acaso)
            self.user = self.scope.get('user')

        # Validar autenticación y membresía
        if not await self.is_user_authorized():
            await self.close(code=4003)  # Forbidden
            return

        self.room_group_name = f'diagram_{self.diagram_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    @database_sync_to_async
    def is_user_authorized(self):
        """Verifica si el usuario está autenticado y es miembro del proyecto."""
        # Verificar autenticación
        if isinstance(self.user, AnonymousUser) or not self.user.is_authenticated:
            return False
            
        try:
            # Obtener el diagrama y su proyecto
            diagram = Diagram.objects.select_related('project').get(id=self.diagram_id)
            
            # Verificar si es miembro del proyecto
            return ProjectMember.objects.filter(
                project=diagram.project,
                user=self.user
            ).exists()
            
        except Diagram.DoesNotExist:
            return False

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            # Intenta parsear como JSON
            data = json.loads(text_data)
        except json.JSONDecodeError:
            # Si no es JSON válido, crea un objeto básico
            data = {'type': 'message', 'content': text_data}
        
        # Envía a todos los conectados al mismo diagrama
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'diagram_event',
                'message': data,  # Envía el objeto, no solo texto
            }
        )

    async def diagram_event(self, event):
        # Envía como JSON al frontend
        await self.send(text_data=json.dumps(event['message']))