import json
from datetime import datetime, timezone
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from Apps.modeling.models import Diagram
from Apps.workspace.models import ProjectMember
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

class DiagramConsumer(AsyncWebsocketConsumer):
    # Diccionario para rastrear usuarios activos por diagrama
    active_users = {}

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
        
        # Agregar al grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        
        # Agregar usuario a la lista de activos
        await self.add_active_user()
        
        # Notificar a todos los usuarios sobre la lista actualizada
        await self.broadcast_active_users()
        
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

    async def add_active_user(self):
        """Agregar usuario a la lista de activos del diagrama."""
        if self.diagram_id not in self.active_users:
            self.active_users[self.diagram_id] = {}
        
        # Almacenar información del usuario
        self.active_users[self.diagram_id][self.channel_name] = {
            'id': str(self.user.id),
            'username': self.user.username,
            'email': self.user.email,
            'connected_at': datetime.now(timezone.utc).isoformat()
        }

    async def remove_active_user(self):
        """Remover usuario de la lista de activos del diagrama."""
        if (self.diagram_id in self.active_users and 
            self.channel_name in self.active_users[self.diagram_id]):
            del self.active_users[self.diagram_id][self.channel_name]
            
            # Si no quedan usuarios, limpiar el diagrama
            if not self.active_users[self.diagram_id]:
                del self.active_users[self.diagram_id]

    async def broadcast_active_users(self):
        """Enviar lista de usuarios activos a todos los conectados."""
        if self.diagram_id in self.active_users:
            # Crear lista de usuarios únicos (por si hay múltiples conexiones del mismo usuario)
            users_dict = {}
            for user_data in self.active_users[self.diagram_id].values():
                user_id = user_data['id']
                if user_id not in users_dict:
                    users_dict[user_id] = {
                        'id': user_data['id'],
                        'username': user_data['username'],
                        'email': user_data['email']
                    }
            
            users_list = list(users_dict.values())
        else:
            users_list = []

        # Enviar evento de usuarios activos
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'active_users_update',
                'users': users_list
            }
        )

    async def disconnect(self, close_code):
        # Remover usuario de activos
        await self.remove_active_user()
        
        # Notificar cambios a usuarios restantes
        await self.broadcast_active_users()
        
        # Salir del grupo
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            # Intenta parsear como JSON
            data = json.loads(text_data)
        except json.JSONDecodeError:
            # Si no es JSON válido, crea un objeto básico
            data = {'type': 'message', 'content': text_data}
        
        # Manejar diferentes tipos de mensajes
        message_type = data.get('type', 'message')
        
        if message_type == 'request_active_users':
            # Cliente solicita lista de usuarios activos
            await self.broadcast_active_users()
        elif message_type == 'editing_presence':
            # Manejar evento de presencia de edición
            await self.handle_editing_presence(data)
        elif message_type == 'move_element':
            # Reenviar eventos move_element a todos los clientes
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'move_element_broadcast',
                    'event_data': data
                }
            )
        else:
            # Reenviar mensaje a todos los conectados con información del remitente
            message_with_sender = data.copy()
            message_with_sender['senderId'] = str(self.user.id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'diagram_event',
                    'message': message_with_sender,
                    'user': {
                        'id': str(self.user.id),
                        'username': self.user.username
                    }
                }
            )

    async def handle_editing_presence(self, data):
        """
        Recibe el evento editing_presence y lo reenvía a todos los usuarios conectados (excepto el emisor)
        en el formato que espera el frontend.
        """
        # Estructura que espera el frontend:
        # {
        #   "type": "editing_presence",
        #   "data": [
        #     {
        #       "userId": "5",
        #       "username": "andre",
        #       "elementId": "class_1758768945125",
        #       "elementType": "class",
        #       "elementName": "hola",
        #       "action": "start"
        #     }
        #   ]
        # }
        payload = data.get('payload', {})
        # Convertir a lista para cumplir con la estructura esperada
        editing_event = {
            "type": "editing_presence",
            "data": [
                {
                    "userId": payload.get("userId", ""),
                    "username": payload.get("username", ""),
                    "elementId": payload.get("elementId", ""),
                    "elementType": payload.get("elementType", ""),
                    "elementName": payload.get("elementName", ""),
                    "action": payload.get("action", "")
                }
            ]
        }
        # Enviar a todos los usuarios conectados EXCEPTO al emisor
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "editing_presence_broadcast",
                "editing_event": editing_event,
                "sender_channel": self.channel_name
            }
        )

    async def editing_presence_broadcast(self, event):
        # No reenviar al emisor
        if event.get("sender_channel") == self.channel_name:
            return
        await self.send(text_data=json.dumps(event["editing_event"]))

    async def diagram_event(self, event):
        """Manejar eventos generales del diagrama."""
        await self.send(text_data=json.dumps(event['message']))

    async def active_users_update(self, event):
        """Manejar actualización de usuarios activos."""
        message = {
            'type': 'active_users',
            'payload': event['users']
        }
        await self.send(text_data=json.dumps(message))

    async def move_element_broadcast(self, event):
        """Manejar broadcast de eventos move_element (incluyendo editing_presence)."""
        await self.send(text_data=json.dumps(event['event_data']))