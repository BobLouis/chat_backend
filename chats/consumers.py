from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Conversation, Message

from django.contrib.auth import get_user_model
from .serializers import MessageSerializer

import json
from uuid import UUID


"""
This is an overridden method from the json.JSONEncoder class. 
It's called by the json module when it encounters an object that 
it doesn't know how to serialize (convert to JSON).
"""


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


"""

 this custom JSON encoding is crucial when you're dealing with data 
 that includes UUIDs (like messages or conversation identifiers 
 in your chat application). When sending JSON data through WebSockets, 
 all data must be serialized into a string format, and the UUIDEncoder 
 ensures that UUIDs are properly converted into a string format that can 
 be sent over the WebSocket connection.
"""

User = get_user_model()


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    @classmethod
    def encode_json(cls, content):
        return json.dumps(content, cls=UUIDEncoder)

    def connect(self):
        print("Connected!")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            print("user not authenticated!")
            return

        self.accept()
        self.conversation_name = (
            f"{self.scope['url_route']['kwargs']['conversation_name']}"
        )
        self.conversation, created = Conversation.objects.get_or_create(
            name=self.conversation_name
        )

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        self.send_json(
            {
                "type": "online_user_list",
                "users": [user.username for user in self.conversation.online.all()],
            }
        )

        async_to_sync(self.channel_layer.group_send)(
            self.conversation_name,
            {
                "type": "user_join",
                "user": self.user.username,
            },
        )

        self.conversation.online.add(self.user)

        messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
        # self.send_json({
        #     "type": "last_50_messages",
        #     "messages": MessageSerializer(messages, many=True).data,
        # })

        messages = self.conversation.messages.all().order_by("-timestamp")[0:50]
        message_count = self.conversation.messages.all().count()
        self.send_json(
            {
                "type": "last_50_messages",
                "messages": MessageSerializer(messages, many=True).data,
                "has_more": message_count > 50,
            }
        )

    def disconnect(self, code):
        if self.user.is_authenticated:  # send the leave event to the room
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "user_leave",
                    "user": self.user.username,
                },
            )
            self.conversation.online.remove(self.user)
        return super().disconnect(code)

    # async_to_sync(self.channel_layer.group_send) method is used to send a message to a group.
    def chat_message_echo(self, event):
        print(event)
        self.send_json(event)

    def user_join(self, event):
        self.send_json(event)

    def user_leave(self, event):
        self.send_json(event)

    def receive_json(self, content, **kwargs):
        message_type = content["type"]
        if message_type == "greeting":
            print(content["message"])
            self.send_json(
                {
                    "type": "greeting_response",
                    "message": "How are you?",
                }
            )
        if message_type == "chat_message":

            message = Message.objects.create(  # save the message to the database
                from_user=self.user,
                to_user=self.get_receiver(),
                content=content["message"],
                conversation=self.conversation,
            )
            async_to_sync(self.channel_layer.group_send)(
                self.conversation_name,
                {
                    "type": "chat_message_echo",
                    "name": self.user.username,
                    "message": MessageSerializer(message).data,
                },
            )

        return super().receive_json(content, **kwargs)

    def get_receiver(self):
        usernames = self.conversation_name.split("__")
        for username in usernames:
            if username != self.user.username:
                # This is the receiver
                return User.objects.get(username=username)
