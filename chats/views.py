from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet
from .models import Conversation
 
from .serializers import ConversationSerializer
 
 
# class ConversationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
#     serializer_class = ConversationSerializer
#     queryset = Conversation.objects.none()
#     lookup_field = "name"
 
#     def get_queryset(self):
#         queryset = Conversation.objects.filter(
#             name__contains=self.request.user.username
#         )
#         return queryset
 
#     def get_serializer_context(self):
#         return {"request": self.request, "user": self.request.user}


class ConversationViewSet(ModelViewSet):
    serializer_class = ConversationSerializer
    queryset = Conversation.objects.none()
    http_method_names = ['get'] 

    def get_queryset(self):
        return Conversation.objects.filter(name__contains=self.request.user.username)

    def get_serializer_context(self):
        return {"request": self.request, "user": self.request.user}