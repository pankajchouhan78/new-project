from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        username = data.get('username')
        if User.objects.filter(username=username).exists():
            # user = User.objects.get(username=username)
            user = authenticate(username=username, password=data.get('password'))
            if user is None:
                return serializers.ValidationError("Invalid Password")
            return user
        else:
            return serializers.ValidationError("Invalid Username")



            

# class UserSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     username = serializers.CharField(max_length=50)
#     first_name = serializers.CharField(max_length=50)
#     last_name = serializers.CharField(max_length=50)
#     password = serializers.CharField(max_length=255)

    # def validate(self, data):
    #     username = data.get('username')
    #     if User.objects.filter(username=username).exists:
    #         return  ValidationError("Username is already in use")
    #     return data

    # def create(self,validated_data):
    #     return User.objects.create(**validated_data)
    
    # def update(self, instance, validated_data):
    #     instance.username = validated_data.get('username', instance.username)
    #     instance.first_name = validated_data.get('first_name', instance.first_name)
    #     instance.last_name = validated_data.get('last_name', instance.last_name)
    #     instance.language = validated_data.get('language', instance.language)
    #     instance.password = validated_data.get('password', instance.password)
    #     instance.save()
    #     return instance



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password is not None:
            user.password = make_password(password)
            user.save()
        return user
    
    def update(self,instance, validated_data):
        password = validated_data.pop('password',None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)
# 
# 
# 
def validate(self, data):
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
# 
        if name == 'admin':
            raise serializers.ValidationError('Invalid name')
        if email == 'admin@example.com':
            raise serializers.ValidationError('Invalid email')
        if message == 'spam':
            raise serializers.ValidationError('Invalid message')
        return data    
# 
# 


class PersonSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Person
        fields = "__all__"