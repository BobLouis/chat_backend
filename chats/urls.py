from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register("conversations", ConversationViewSet, basename="conversations")

urlpatterns = [
    path("", include(router.urls)),
]
