from users.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import Tweet
from .serializers import TweetSerializer

from django.db import transaction


class TweetsView(APIView):
    def get(self, request):
        tweets = Tweet.objects.all()
        serializer = TweetSerializer(tweets, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        if request.user.is_authenticated:
            serializer = TweetSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    tweet = serializer.save(user=request.user)
                    return Response(TweetSerializer(tweet).data)
            else:
                return Response(serializer.errors)

class TweetDetailsView(APIView):
    def get_object(self, pk):
        try:
            return Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound(detail="Tweet Not Found")
        
    def get(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet)
        return Response(serializer.data)  
    
    def put(self, request, pk):
        tweet = self.get_object(pk)
        serializer = TweetSerializer(tweet, data=request.data, partial=True)
        if serializer.is_valid():
            updated_tweet = serializer.save()
            return Response(TweetSerializer(updated_tweet).data)
        else:
            return Response(serializer.errors)
    
    def delete(self, request, pk):
        tweet = self.get_object(pk)
        if not request.user.is_authenticated:
            raise NotAuthenticated
        if tweet.user != request.user:
            raise PermissionDenied
        tweet.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class UserTweetsView(APIView):        

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound(detail="User not found")

        user_tweets = user.tweets.all()  # Access user's tweets using related_name
        serializer = TweetSerializer(user_tweets, many=True)
        return Response(serializer.data)  
    

# @api_view(["GET"])
# def show_all_tweets(request):
#     tweets = Tweet.objects.all()
#     serializer = TweetSerializer(tweets, many=True)
#     return Response(serializer.data)

# @api_view(["GET"])
# def show_all_user_tweets(request, user_id):
#     try:
#         user = User.objects.get(pk=user_id)
#     except User.DoesNotExist:
#         raise NotFound(detail="User not found")

#     user_tweets = user.tweets.all()  # Access user's tweets using related_name
#     serializer = TweetSerializer(user_tweets, many=True)
#     return Response(serializer.data)
