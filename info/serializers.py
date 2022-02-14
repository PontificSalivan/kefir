from rest_framework import serializers
from .models import Person
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['name', 'favorite_colour', 'favorite_food', ]


class UserCurrentSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(method_name='get_admin')

    class Meta:
        model = Person
        fields = ['user_id', 'name', 'favorite_colour', 'favorite_food', 'is_admin']

    @staticmethod
    def get_admin(user):
        return user.user_id.is_superuser


class PrivateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['user_id', 'name', 'secret_word', 'favorite_colour', 'favorite_food', ]


class PrivateUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['name', 'secret_word', 'favorite_colour', 'favorite_food', ]


class PrivateUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = ['user_id', 'name', 'secret_word', ]
