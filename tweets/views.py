from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet

def show_all_tweets(request):
    try:
        tweets = Tweet.objects.all()
        return render(request, "all_tweets.html", {"tweets": tweets})
    except Tweet.DoesNotExist:
        return render(request, "all_tweets.html", {"not_found": True})