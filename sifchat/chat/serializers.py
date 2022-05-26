from rest_framework import serializers
from account.serializers import *
from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        depth = 2
