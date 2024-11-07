from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from .models import Tweet
from .serializers import TweetSerializer

@api_view(["GET"])
def show_all_tweets(request):
    tweets = Tweet.objects.all()
    serializer = TweetSerializer(tweets, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def show_all_user_tweets(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise NotFound(detail="User not found")

    user_tweets = user.tweets.all()  # Access user's tweets using related_name
    serializer = TweetSerializer(user_tweets, many=True)
    return Response(serializer.data)
