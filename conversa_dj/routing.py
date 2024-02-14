
from django.urls import path
 
from chats.consumers import ChatConsumer
 
websocket_urlpatterns = [
    
    
    path("chat/<str:conversation_name>/", ChatConsumer.as_asgi())
    
]