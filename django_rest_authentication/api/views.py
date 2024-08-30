from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from django.contrib.auth.models import User
from .models import *
from .serializer import *

# Create your views here.
def index(request):
    return HttpResponse("this index")

class UserView(APIView):
    def get(self,request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookViewLIst(APIView):
    permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    def get(self,request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data, status=200)
    
class BookView(APIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self,request):
        # print(f"User: {request.user}")
        # print(f"Auth: {request.auth}")
        request.data['user'] = 1
        # request.data['user'] = request.user.id

        serializer = BookSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)