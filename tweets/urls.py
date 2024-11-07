from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/tweets/', views.show_all_tweets),
    path('api/v1/users/<int:user_id>/tweets/', views.show_all_user_tweets),
]
