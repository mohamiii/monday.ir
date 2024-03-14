from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    @staticmethod
    def validate_email(value):
        """validates emails: emails have to be from gmail, emails will be lower-cased"""
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email exists!")
        if "@gmail" not in value:
            raise serializers.ValidationError("Only Gmail is allowed.")
        return lower_email

    @staticmethod
    def validate_username(value):
        """validates usernames: admin or duplicate usernames not allowed"""
        if 'admin' in value.lower():
            raise serializers.ValidationError('Username can\'t be admin')
        return value

    class Meta:
        model = User
        fields = ("id",
                  "last_login",
                  "username",
                  "first_name",
                  "last_name",
                  "email",
                  "is_active",
                  "date_joined",
                  "groups",
                  "user_permissions",
                  )
        extra_kwargs = {
            'id': {'read_only': True},
            'date_joined': {'read_only': True},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True},
        }


class UserRegisterSerializer(UserSerializer):
    passwordConfirm = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'passwordConfirm', 'first_name', 'last_name')
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


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password_confirm = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
