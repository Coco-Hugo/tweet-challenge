from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer

from django.db import transaction
from django.contrib.auth import authenticate, login, logout


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError
        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            new_user = serializer.save()
            new_user.set_password(password)# Never do this: new_user.password = password (unhashed)
            serializer = UserSerializer(new_user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        

class UserDetailsView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise NotFound(detail="User Not Found")
        
    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)  
    
    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            return Response(UserSerializer(updated_user).data)
        else:
            return Response(serializer.errors) 
    
    def delete(self, request, pk):
        user = self.get_object(pk)  
        if not request.user.is_authenticated:
            raise NotAuthenticated
        user.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class EditPassword(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_pw = request.data.get("old_password")
        new_pw = request.data.get("new_password")
        if not old_pw or not new_pw:
            raise ParseError
        if user.check_password(old_pw):
            user.set_password(new_pw)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
            

class LogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user) # Create session and send cookies to user
            return Response({"ok": "Welcome!"})
        else:
            return Response({"error": "Wrong Password"})
        
        
class LogOut(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        logout(request)
        return Response({"ok":"Goodbye"})