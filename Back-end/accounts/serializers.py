from rest_framework import serializers
from django.contrib.auth.models import User


def validate_email(value):
    lower_email = value.lower()
    if User.objects.filter(email__iexact=lower_email).exists():
        raise serializers.ValidationError("Email exists!")
    if "@gmail" not in value:
        raise serializers.ValidationError("Only Gmail!")
    return lower_email


def validate_username(value):
    if value == 'admin':
        raise serializers.ValidationError('Username can\'t be `admin`')
    return value


class UserRegisterSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'passwordConfirm')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'validators': (validate_email,)},
            'username': {'validators': (validate_username,)}
        }

    def create(self, validated_data):
        del validated_data['passwordConfirm']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError('password does not match')
        return data
