from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    passwordConfirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'passwordConfirm')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        del validated_data['passwordConfirm']
        return User.objects.create_user(**validated_data)

    def validate(self, data):
        """validates passwords: passwords must contain 8 characters with numbers and digits"""
        if data['password'] != data['passwordConfirm']:
            raise serializers.ValidationError('Passwords do not match')

        min_length = 8

        if len(data['password']) < min_length:
            raise serializers.ValidationError('Password must be at least {0} characters long.'.format(min_length))

        # check for digit
        if not any(char.isdigit() for char in data['password']):
            raise serializers.ValidationError('Password must contain at least 1 digit.')

        # check for letter
        if not any(char.isalpha() for char in data['password']):
            raise serializers.ValidationError('Password must contain at least 1 letter.')

        return data

    def validate_email(self, value):
        """validates emails: emails have to be from gmail, emails will be lower-cased"""
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email exists!")
        if "@gmail" not in value:
            raise serializers.ValidationError("Only Gmail is allowed.")
        return lower_email

    def validate_username(self, value):
        """validates usernames: admin or duplicate usernames not allowed"""
        if 'admin' in value.lower():
            raise serializers.ValidationError('Username can\'t be admin')
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
