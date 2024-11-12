from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/', views.UsersView.as_view()),
    path('api/v1/users/<int:pk>/', views.UserDetailsView.as_view()),
]
