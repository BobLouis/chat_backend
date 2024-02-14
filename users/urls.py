
from django.urls import path
from .views import register_user, login_user, get_all_users
urlpatterns = [

    path('register/', register_user),
    path('login/', login_user),
    path('all/', get_all_users, name='get_all_users'),


]