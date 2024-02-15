from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from .paginaters import MessagePagination
 
 

class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    http_method_names = ['get'] 

    def get_queryset(self):
        return Conversation.objects.filter(name__contains=self.request.user.username)

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}
    

class MessageViewSet(ModelViewSet):
    serializer_class = MessageSerializer
    queryset = Message.objects.none()
    pagination_class = MessagePagination
    http_method_names = ['get'] 
 
    def get_queryset(self):
        conversation_name = self.request.GET.get("conversation")
        queryset = (
            Message.objects.filter(
                conversation__name__contains=self.request.user.username,
            )
            .filter(conversation__name=conversation_name)
            .order_by("-timestamp")
        )
        return queryset