from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/users/', views.UsersView.as_view()),
    path('api/v1/users/<int:pk>/', views.UserDetailsView.as_view()),
    path('api/v1/users/password', views.EditPassword.as_view()),
    path('api/v1/users/login', views.LogIn.as_view()),
    path('api/v1/users/logout', views.LogOut.as_view()),
]
