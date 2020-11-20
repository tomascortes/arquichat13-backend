from django.test import TestCase

    def test_new_chat_room(self):
        response = self.client.get(reverse('room', args=['test_room']))
        response = json.loads(response.content)
        self.assertEqual(response, {'alias': 'anon', 'room_topic': 'test_room', 'messages': []}) 

