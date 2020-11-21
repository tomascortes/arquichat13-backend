from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

from .models import ChatRoom, Message, Request, Admin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import socket
import json
#from django import forms
from django.contrib.auth.models import User


from django.db import connection
from datetime import datetime

from urllib.parse import unquote


def index(request):
    rooms = ChatRoom.objects.all()
    str_rooms = [str(room) for room in rooms]
    response = HttpResponse(json.dumps(str_rooms))

    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def room(request, room_name, css, js):
    try:
        room = ChatRoom.objects.get(topic=room_name)
        if room.private:
            return redirect("/chat/")
        messages = [m.text for m in room.message_set.all().order_by('date', 'text')]
    except ChatRoom.DoesNotExist:
        room = ChatRoom.create(room_name, css, js)
        room.save()
        messages = []
    try:
        alias = request.session['alias']
    except:
        alias = "anon"
    
    response = HttpResponse(json.dumps({
        'alias': alias,
        'room_topic': room_name,
        'messages': messages,
        'css': room.css,
        'js': room.js
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
        admin = Admin(user=user, is_admin=False)
        admin.save()
        login(request, user)
        response = HttpResponse('')
    except:
        response = HttpResponse('Bad combination', status=400)
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def register_admin(request, username, password, key):
    if key != "wololo":
        response = HttpResponse('Bad combination', status=400)
    else:
        try:
            user = User(username=username)
            user.set_password(password)
            user.save()
            admin = Admin(user=user, is_admin=True)
            admin.save()
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

def sign_in_admin(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        u = User.objects.get(username=username)
        if u.admin.is_admin:
            login(request, user)
            response = HttpResponse('')
        else:
            response = HttpResponse('Not an Admin', status=403)
    else:
        response = HttpResponse('Authentication error', status=401)
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def sign_out(request, username, password):
    print(username, password)
    logout(request)
    response = HttpResponse('')
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response


def redirect_view(request):
    body = json.loads(request['body'])
    try:
        alias = body['alias']
        request.session['alias'] = alias
    except KeyError:
        pass
    room_name = body['room']
    room = room_name
    return redirect(f'/chat/{room}/')


def verify_admin(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        u = User.objects.get(username=username)
        if u.admin.is_admin:
            return True
        return False
    return False 


def delete_message(request, room_name, message):
    # if not verify_admin(username, password):
    #     response = HttpResponse('')
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        print("A", message)
        message = unquote(message).replace(" ", "")
        print("B", message)
        room = ChatRoom.objects.get(topic=room_name)
        print("--")

        message_ = [m for m in room.message_set.all() if m.text.replace(" ", "")==message][0]
        print("C", message_)
        message_.delete()
        print("D")
        response = HttpResponse('')
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def delete_room(request, room_name):
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        room = ChatRoom.objects.get(topic=room_name)
        print("A")
        room.delete()
        print("B")
        response = HttpResponse('')
        print("C")
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except ChatRoom.DoesNotExist:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    


def edit_message(request, room_name, message, new_message):
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        print("A", message, "-")
        message = unquote(message).replace(" ", "")
        print("B", message, "-", new_message)
        new_message = unquote(new_message)
        print("C", new_message)
        room = ChatRoom.objects.get(topic=room_name)
        print("--")
        messages_ = [m for m in room.message_set.all() if m.text.replace(" ", "")==message]
        print(messages_)
        print("D")
        print(messages_[0])
        message_ = messages_[0]
        print(type(room), type(message_))
        message_.text = new_message
        print("E")
        message_.save()
        print("F")
        response = HttpResponse('Reload Required', status=200)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def edit_room(request, room_name, css, js):  # only change css and js
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        room = ChatRoom.objects.get(topic=room_name)
        room.css = css
        room.js = js
        room.save()
        response = HttpResponse('Privacy changed', status=200)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def edit_room_privacy(request, room_name):  # only change privacy
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        room = ChatRoom.objects.get(topic=room_name)
        if room.private:
            room.private = False
        else:
            room.private = True
        room.save()
        response = HttpResponse('Privacy changed', status=200)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    

def delete_user(request, username):
    # if not verify_admin(admin, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        u = User.objects.get(username=username)
        u.delete()
        response = HttpResponse('User deleted', status=200)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def create_req(request, room_name, css, js):
    try:
        print("A")
        room = ChatRoom.objects.get(topic=room_name)
        print("B")
        req = Request(id=None, room=room, css=css, js=js)
        print("C")
        req.save()
        print("D")
        response = HttpResponse('')
        print("E")
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def room_requests(request, room_name):
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        room = ChatRoom.objects.get(topic=room_name)
        reqs = [{'css': r.css, 'js': r.js} for r in room.request_set.all()]
        response = HttpResponse(json.dumps({
            'room_topic': room_name,
            'requests': reqs,
            'css': room.css,
            'js': room.js
        }))
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    



def delete_requests(request, room_name):
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        room = ChatRoom.objects.get(topic=room_name)
        room.request_set.all().delete()
        response = HttpResponse('Deleted', status=200)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response


def admin_room(request):
    # if not verify_admin(username, password):
    #     response = HttpResponse('Authentication error', status=401)
    #     host = socket.gethostbyname(socket.gethostname())
    #     response.__setitem__('host_ip', host)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     return response
    try:
        rooms = [room.topic for room in ChatRoom.objects.all()]
        users = [u.username for u in User.objects.all()]
        response = HttpResponse(json.dumps({
            'users': users,
            'rooms': rooms
        }))
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response
    except:
        response = HttpResponse('Bad request', status=400)
        host = socket.gethostbyname(socket.gethostname())
        response.__setitem__('host_ip', host)
        response['Access-Control-Allow-Origin'] = '*'
        return response

def check(request):
    response = HttpResponse(status=200)
    host = socket.gethostbyname(socket.gethostname())
    response.__setitem__('host_ip', host)
    response['Access-Control-Allow-Origin'] = '*'
    return response
