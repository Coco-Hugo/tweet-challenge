from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.Serializer):
    
    payload = serializers.CharField(max_length=180)
    user = serializers.CharField()