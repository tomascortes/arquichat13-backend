import json
from channels.generic.websocket import AsyncWebsocketConsumer
from datetime import datetime
from .models import ChatRoom, Message
import aiohttp  # , requests
import json
import boto3
import os

def api_call_sns(string_to_send):
    AWS_ACCESS_ID = os.environ.get('AWS_ACCESS_ID')
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
    AWS_ARN = os.environ.get('AWS_ARN')
    sns_client = boto3.client(
        'sns',
        aws_access_key_id=AWS_ACCESS_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name="us-east-2"
    )
    response = sns_client.publish(
        TopicArn=AWS_ARN, 
        Message=string_to_send,
        Subject="EMAIL")
    return response

async def rget(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def rpost(url, json):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=json) as resp:
            return await resp.json()

def obtain_user_email(word_list):
    #return a list with all contacts that where tagged
    tagged = list()
    for i in range(len(word_list)):
        if "#" in word_list[i] and "@" in word_list[i]:
            tagged.append(word_list[i].strip("#"))
    return tagged
            



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        init = json.loads(text_data)['message']

        pre_filtered = init.split(" ")
        alias = pre_filtered.pop(0)
        body_filtrado = await rget('https://z2wnq9fjzi.execute-api.us-east-1.amazonaws.com/dev/filtering?text=' + " ".join(pre_filtered).replace(" ", "%20").replace('#', '%23'))
        words = [alias] + body_filtrado.split(" ")
        cmd = words[1]
        tagged = obtain_user_email(words)
        for person in tagged:
            to_send = dict()
            to_send["email"] = person
            to_send["message"] = " ".join(words)
            string_to_send = json.dumps(to_send)
            api_call_sns(string_to_send)

        print('words:', words, end="\n\n")
        try:
            room = ChatRoom.objects.get(topic=self.room_name)
        except ChatRoom.DoesNotExist:
            pass
        if cmd == "\private":
            if room.private:
                room.private = False
                final = "ROOM SET TO PUBLIC"
            else:
                room.private = True
                final = "ROOM SET TO PRIVATE"
            room.save()     
        elif cmd == "\kanye":  # for random Kanye West quotes 
            response = await rget('https://api.kanye.rest')
            final = "KANYE SAYS: " + response['quote']
        elif cmd == "\morse": 
            try:
                text2 = " ".join(words[2:])
                r = await rpost('https://api.funtranslations.com/translate/morse.json', json={"text": text2})
                final = alias + r["contents"]['translated']
            except:
                final = alias + " ".join(words[2:]) + "(to many translations)"
        else:
            final = " ".join(words)
        
        message = "(" + datetime.now().ctime() + ")" + final

        # Save message and send message to room group
        m = Message(id=None, text=message, room=room)
        m.save()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
