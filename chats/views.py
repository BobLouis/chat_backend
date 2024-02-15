from rest_framework.viewsets import ModelViewSet
from .models import Conversation
 
from .serializers import ConversationSerializer
 
 

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    http_method_names = ['get'] 

    def get_queryset(self):
        return Conversation.objects.filter(name__contains=self.request.user.username)

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}