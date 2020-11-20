from django.db import models
from django.contrib.auth.models import User

#class User(AbstractUser):
    #is_admin = models.BooleanField(default=False)

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class ChatRoom(models.Model):
    topic = models.CharField(max_length=255)
    private = models.BooleanField(default=False)
    css = models.CharField(max_length=255, default='')
    js = models.CharField(max_length=255, default='')

    def __str__(self):
        return str({
            'topic': self.topic, 
            'private': self.private,
            'css': self.css,
            'js': self.js
        })
        
    @classmethod
    def create(cls, topic, css, js):
        room = cls(topic=topic, css=css, js=js, private=False)
        return room


class Message(models.Model):
    text = models.CharField(max_length=255)
    original = models.CharField(max_length=255, default=text)
    date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Request(models.Model):
    css = models.CharField(max_length=255)
    js = models.CharField(max_length=255)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return str({
            'css': self.css,
            'js': self.js
        })
