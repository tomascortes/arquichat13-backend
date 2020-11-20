from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/<str:css>/<str:js>', views.room, name='room'),
]