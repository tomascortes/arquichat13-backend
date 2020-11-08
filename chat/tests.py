from django.test import TestCase
from django.urls import reverse
from .models import ChatRoom
import json
# Create your tests here.

class ChatTests(TestCase):
    def test_chat_endpoint(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
    
    def test_chat_rooms(self):
        ChatRoom.objects.create(topic='TestRoom')
        response = self.client.get(reverse('index'))
        response = json.loads(response.content)
        self.assertQuerysetEqual(response, ['"{\'topic\': \'TestRoom\', \'private\': False}"'])

    def test_new_chat_room(self):
        response = self.client.get(reverse('room', args=['test_room']))
        response = json.loads(response.content)
        self.assertEqual(response, {'alias': 'anon', 'room_topic': 'test_room', 'messages': []})