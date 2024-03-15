from django.urls import path
from base import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/', views.room, name="room"),
]
