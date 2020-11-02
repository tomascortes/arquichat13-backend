from django.db import models

class ChatRoom(models.Model):

    topic = models.CharField(max_length=255)
    private = models.BooleanField(default=False)

    def __str__(self):
        return str({'topic': self.topic, 'private': self.private})
        
    @classmethod
    def create(cls, topic):
        room = cls(topic=topic, private=False)
        # do something with the book
        return room

    # @property
    # def group_name(self):
    #     """
    #     Returns the Channels Group name that sockets should subscribe to to get sent
    #     messages as they are generated.
    #     """
    #     return "room-%s" % self.id

class Message(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
