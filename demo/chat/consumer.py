 
from asgiref.sync import async_to_sync,sync_to_async
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer,SyncConsumer,AsyncConsumer
from .models import Users
from django.core.serializers import serialize
from channels.db import database_sync_to_async
from channels.auth import get_user,login,logout
from django.contrib.auth.models import AnonymousUser
from channels.layers import get_channel_layer


import json
import random

@database_sync_to_async
def get_name(self):
    return Users.objects.all()[2].msg
@database_sync_to_async
def set_name(self):
    Users.objects.create(msg=self.channel_name)

@database_sync_to_async
def destroy(self):
    Users.objects.filter(msg=self.channel_name).delete()
    

# class Test(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         print("connect")
#     async def receive(self, text_data=None, bytes_data=None):
#         name=await get_name(self)
#         print(name)
    
#         await self.channel_layer.send(
#              self.channel_name,
#              {"type": "chat.message", "message": text_data}
#         )

#         await self.channel_layer.send(
#              name
#            ,
#              {"type": "chat.message", "message": text_data}
#         )
#         # print(text_data)
#         # await self.send(text_data=text_data)

#     async def chat_message(self, event):
#         # Handles the "chat.message" event when it's sent to us.
#         await self.send(text_data=event["message"])

#     async def disconnect(self, code):
#         print("disconnect")

# class GetConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         await set_name(self)
#         # await sync_to_async(Users.objects.create)(msg=self.channel_name)
#     async def disconnect(self, code):
#         await destroy(self)
#         print("get disconnect")
        
   
#     async def chat_message(self, event):
#         # Handles the "chat.message" event when it's sent to us.
#         await self.send(text_data=event["message"])


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")

        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()


    async def disconnect(self, code):
        print("disconnect")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)


    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
             self.room_group_name, {"type": "chat.message", "message": message,"user":self.scope["user"].username}
        )


    async def chat_message(self, event):
        message = event["message"]
        user=event["user"]
        # print(user)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message":message,"user":user}))
    