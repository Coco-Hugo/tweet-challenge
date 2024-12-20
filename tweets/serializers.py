from rest_framework import serializers
from .models import Tweet
from users.serializers import UserSerializer

class TweetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = "__all__"

# class TweetSerializer(serializers.Serializer):
#     payload = serializers.CharField(max_length=180)
#     user = serializers.CharField()