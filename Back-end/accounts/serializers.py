from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.models import User

##############

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],

        )

        return user

    class Meta:
        model = UserModel
        # serialized model fields
        fields = ("id", "username", "password")


##############


def clean_email(value):
    if 'gmail' not in value:
        raise serializers.ValidationError('Invalid email')


def validate_username(value):
    if value == 'admin':
        raise serializers.ValidationError('Username can\'t be `admin`')
    return value


class UserRegisterSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'passwordConfirm')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (clean_email,)}
        }

    def create(self, validated_data):
        del validated_data['passwordConfirm']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError('password does not match')
        return data
