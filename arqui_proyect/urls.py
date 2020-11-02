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
    path('redirect/', v.redirect_view),
    path('accounts/login/<str:username>/<str:password>/', v.sign_in),
    path('accounts/logout/<str:username>/<str:password>/', v.sign_out),
    path('chat/', include('chat.urls')),
    path('admin/', admin.site.urls),
]