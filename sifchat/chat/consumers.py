import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from pytz import timezone


from account.models import UserProfile
from django.contrib.auth.models import User
from django.db.models import Q
from .models import *
from django.core import serializers as cserializer
from .serializers import *
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self, message):

        fname = self.scope.get('url_route').get('kwargs').get('fromusername')
        sname = self.scope.get('url_route').get('kwargs').get('tousername')

        thread_obj = await self.get_thread(fname, sname)

        self.thread_obj = thread_obj

        chat_room = f'room_{thread_obj.id}'

        self.chat_room = chat_room

        self.msgs = await self.get_all_msg_of_the_thread(self.thread_obj)

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps(
            {
                "type": "allmessage",
                "messages": self.msgs
            }
        ))

    async def websocket_receive(self, message):

        msg = await self.save_chat_message(self.thread_obj, self.sender, message.get('text'))
        await self.channel_layer.group_send(
            self.chat_room, {
                "type": "send_msg",
                "messages": msg
            }

        )

    async def websocket_disconnect(self, message):
        return await super().websocket_disconnect(message)

    async def send_msg(self, msg):
        await self.send(text_data=json.dumps(
            {
                "type": "newmessage",
                "msg": msg
            }
        ))

    @database_sync_to_async
    def get_thread(self, first, second):
        fp = UserProfile.objects.get(user__username=first)
        sp = UserProfile.objects.get(user__username=second)
        self.sender = fp
        #qlookup1 = Q(first=fp) & Q(second=fp)
        #qlookup2 = Q(first=sp) & Q(second=fp)
        qs = MyThread.objects.filter((Q(first=fp) & Q(second=sp)) | (
            Q(first=sp) & Q(second=fp))).distinct()

        if qs.count() == 0:
            mythread = MyThread.objects.create(first=fp, second=sp)

            return mythread

        else:
            mythread = qs.first()

            return mythread

    @database_sync_to_async
    def get_all_msg_of_the_thread(self, thread_obj):

        msgs = ChatMessage.objects.filter(mythread=thread_obj)
        msgs_json = ChatMessageSerializer(msgs, many=True).data

        return msgs_json

    @database_sync_to_async
    def save_chat_message(self, thread_obj, sender, msg):
        #sndr = UserProfile.objects.get(user__username=sender)
        mg = ChatMessage.objects.create(
            mythread=thread_obj, sender=sender, message=msg)
        sg = ChatMessageSerializer(mg).data
        self.thread_obj.updated = timezone.now()
        self.thread_obj.latest_message = mg
        self.thread_obj.save()
        return sg
