from .serializers import UserSerializer

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from core.utls import response_structure


# Create your views here.
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            data = UserSerializer(user).data
            return Response(response_structure(data, status.HTTP_200_OK, 'Login Successful', False))
        else:
            return Response(response_structure(None, status.HTTP_401_UNAUTHORIZED, 'Invalid Credentials', True))
        
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            password = request.data.get('password')
            user.set_password(password)
            user.save()
            return Response(response_structure(serializer.data, status.HTTP_201_CREATED, 'User created successfully', False))
        else:
            return Response(response_structure(None, status.HTTP_400_BAD_REQUEST, 'User creation failed', True))
        


    

