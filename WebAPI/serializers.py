from rest_framework import serializers
from .models import Books, Books_log, Roles
from django.contrib.auth.models import User


class Books_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class Books_log_serializer(serializers.ModelSerializer):
    class Meta:
        model = Books_log
        fields = '__all__'

class Roles_serializer(serializers.ModelSerializer):
    class Meta:
        model = Roles
        fields = '__all__'