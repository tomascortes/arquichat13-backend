"""arqui_proyect URL Configuration
"""
from django.conf.urls import include
from django.urls import path, re_path
from django.contrib import admin

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from chat import views as v

urlpatterns = [
    path('accounts/register/<str:username>/<str:password>/', v.register),
    path('accounts/register-admin/<str:username>/<str:password>/<str:key>', v.register_admin),
    path('redirect/', v.redirect_view),
    path('accounts/login/<str:username>/<str:password>/', v.sign_in),
    path('accounts/login-admin/<str:username>/<str:password>/', v.sign_in_admin),
    path('accounts/logout/<str:username>/<str:password>/', v.sign_out),
    path('chat/', include('chat.urls')),
    path('admin/<str:username>/<str:password>/', v.admin_room),
    path('admin/room/delete/<str:room_name>/<str:username>/<str:password>/', v.delete_room),
    path('admin/room/edit/<str:room_name>/<str:username>/<str:password>/', v.edit_room),
    path('admin/message/delete/<str:room_name>/<str:message>/<str:username>/<str:password>/', v.delete_message),
    path('admin/message/edit/<str:room_name>/<str:message>/<str:new_message>/<str:username>/<str:password>/', v.edit_message),
    path('admin/user/delete/<str:username>/<str:admin>/<str:password>/', v.delete_user),
    path('request/<str:room_name>/<str:css>/<str:js>', v.create_request),
    path('request/index/<str:room_name>/', v.room_requests),
    path('request/delete/<str:room_name>/', v.delete_requests),
]