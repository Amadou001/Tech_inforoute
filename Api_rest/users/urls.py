from django.urls import path
from .views import register_user, login_user, delete_user, logout_user, register_page, login_page, current_user

urlpatterns = [
    path('register_page/', register_page, name='register_page'),
    path('login_page/', login_page, name='login_page'),
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('delete/', delete_user, name='delete_user'),
    path('logout/', logout_user, name='logout'),
    path("me/", current_user),

]
