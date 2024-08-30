from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import PersonSerializer, UserSerializer, LoginSerializer
from .models import Person
from django.contrib.auth.models import User

from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(['GET', 'POST'])
def person(request):
    if request.method == 'GET':
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = PersonSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PATCH'])
def update_person(request,pk=None):
    try:
        person = Person.objects.get(pk=pk)
    
    except Person.DoesNotExist:
        return Response("Person not found", status = 404)

    serializer = PersonSerializer(instance = person, data = request.data, partial=True)
    if serializer.is_valid:
        serializer.save()
        return Response(serializer.data, status = status.HTTP_100_CONTINUE)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def users(request):
    if request.method == 'GET':
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
    

def get_user(pk=None):
    if pk is None:
        return Response("not found", status=404)
    
    if not User.objects.filter(pk=pk).exists():
        return Response("User not found ", status=status.HTTP_404_NOT_FOUND)

    return User.objects.get(id=pk)
    
@api_view(['GET','PATCH','PUT','DELETE'])
def users_pk(request, pk=None):
    user = get_user(pk)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status= status.HTTP_200_OK)

    if request.method == 'PUT':
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        user.delete()
        return Response("success", status=204)
    
    if request.method == 'PATCH':
        serializer = UserSerializer(instance=user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

#  API View --------------------------------------------------------------
#  
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class check_login(APIView):
    # authentication_classes = [SessionAuthentication, TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        return Response(content)
    
class UserAPIView(APIView):

    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk=None):
        print(f"User: {request.user}")
        print(f"Auth: {request.auth}")
        # import pdb; pdb.set_trace()
        if pk is None:
            user = User.objects.all()
            serializer = UserSerializer(user, many=True)
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            try:
                user = User.objects.get(pk=pk)
                serializer = UserSerializer(user)
                return Response(serializer.data, status = status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response("User not found", status = status.HTTP_400_BAD_REQUEST)
                

    def post(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self,request,pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(instance=user ,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request,pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(instance=user ,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response("User deleted", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)
        
# viewsets ----------------------------------------------------------------

from rest_framework import viewsets
class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request,pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data, status = status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User not found", status = status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(instance=user ,data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self , request,pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(instance=user ,data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response("User deleted", status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_400_BAD_REQUEST)

#  viewsets.modelViewsets ----------------------------------------------

class UserModelViewsets(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


#  generics --------------------------------
from rest_framework import generics

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer