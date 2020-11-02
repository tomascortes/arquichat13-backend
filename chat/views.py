from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import ChatRoom, Message
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import socket
import json
#from django import forms
from django.contrib.auth.models import User


from django.db import connection
from datetime import datetime

# class LoginForm(forms.ModelForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={"class": "input", "placeholder": "username"}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "input", "placeholder": "Contraseña"}))

#     class Meta:
#         model = User
#         fields = ('username', 'password')


def index(request):
    rooms = ChatRoom.objects.all()
    # return render(request, 'chat/index.html', {
    #     "rooms": rooms,
    # })
    str_rooms = [str(room) for room in rooms]
    response = HttpResponse(json.dumps(str_rooms))

    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def room(request, room_name):
    try:
        room = ChatRoom.objects.get(topic=room_name)
        if room.private:
            return redirect("/chat/")
        messages = [m.text for m in room.message_set.all().order_by('date', 'text')]
    except ChatRoom.DoesNotExist:
        room = ChatRoom.create(room_name)
        room.save()
        messages = []
    try:
        alias = request.session['alias']
    except:
        alias = "anon"
    # return render(request, 'chat/room.html', {
    #     'alias': alias,
    #     'room_name': room_name
    # })
    print(messages)
    
    response = HttpResponse(json.dumps({
        'alias': alias,
        'room_topic': room_name,
        'messages': messages
    }))
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def register(request, username, password):
    try:
        user = User(username=username)
        user.set_password(password)
        user.save()
        login(request, user)
        response = HttpResponse('')
    except:
        response = HttpResponse('Bad combination', status=400)
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def sign_in(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        response = HttpResponse('')
    else:
        response = HttpResponse('Authentication error', status=401)
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def sign_out(request, username, password):
    print(username, password)
    logout(request)  # TODO: ?
    response = HttpResponse('')
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def redirect_view(request):
    #if request.method == "POST":
    body = json.loads(request['body'])
    try:
        alias = body['alias']
        request.session['alias'] = alias
    except KeyError:
        pass
    room_name = body['room']
    room = room_name
    return redirect(f'/chat/{room}/')
    # else:
    #     print(request.method)
    #     return redirect('/chat/main/')
