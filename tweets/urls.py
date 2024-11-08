from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/tweets/', views.TweetsView.as_view()),
    path('api/v1/users/<int:user_id>/tweets/', views.UserTweetsView.as_view()),
]
