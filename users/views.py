from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer

from django.db import transaction


class UsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data) 
    
    def post(self, request):
        if request.user.is_authenticated:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                with transaction.atomic():
                    user = serializer.save()
                    return Response(UserSerializer(user).data)
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
