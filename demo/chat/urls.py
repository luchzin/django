from django.urls import path
from django.http import HttpResponse
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("auth/signup",views.signgup_view,name="signup"),
    path("auth/login",views.login_view,name="login"),
    path("chat/<str:room_name>/",views.room, name="room"),
    path("auth/logout",views.logout_view,name="logout"),
    
    
]