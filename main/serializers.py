from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chatbots, Documents
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]  # You can include other fields if needed


class ChatbotSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source="user", read_only=True)

    class Meta:
        model = Chatbots
        fields = ["id", "name", "prompt" , "title" , "isPublic" , "model_type" , "user", "user_details", "date_created"]

class AllChatbotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatbots
        fields = ["id", "name", "title", "user",]



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields = ["id", "documentname", "chatbot", "date_created"]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ("key",)
