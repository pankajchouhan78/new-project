from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, data):
        password = data.pop('password', None)
        user = super().create(data)
        if password is not None:
            user.password = make_password(password)
            user.save()
        return user
    
class BookSerializer(serializers.ModelSerializer):
    def validate_title(self, data):
        title = data
        print(title)
        if title is not None:
            if not title.isalpha():
                raise serializers.ValidationError("contains only alpha characters")
            return title
    class Meta:
        model = Book
        fields = '__all__'