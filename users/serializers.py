from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "email",)

# class TweetSerializer(serializers.Serializer):
#     payload = serializers.CharField(max_length=180)
#     user = serializers.CharField()