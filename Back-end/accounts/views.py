from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework import status, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class UserRegister(APIView):
    @staticmethod
    def post(request):
        validated_data = UserRegisterSerializer(data=request.POST)
        if validated_data.is_valid():
            validated_data.create(validated_data.validated_data)
            return Response(validated_data.data, status=status.HTTP_201_CREATED)
        return Response(validated_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = User.objects.all()

    def list(self, request):
        if request.user.is_staff is not True:
            return Response({'Access denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(instance=self.queryset, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user and request.user.is_staff is not True:
            return Response({'Access denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(instance=user)
        return Response(data=serializer.data)

    def partial_update(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user and request.user.is_staff is not True:
            return Response({'Access denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        validated_data = UserSerializer(instance=user, data=request.POST, partial=True)
        try:
            if validated_data.is_valid():
                validated_data.save()
                return Response(data=validated_data.data)
            return Response(data=validated_data.errors)
        except KeyError:
            return Response({'message': 'Missing a key for validation. Password might be invalid.'})

    def destroy(self, request, pk=None):
        user = get_object_or_404(self.queryset, pk=pk)
        if user != request.user and request.user.is_staff is not True:
            return Response({'Access denied': 'You are not the owner'}, status=status.HTTP_403_FORBIDDEN)
        user.is_active = False
        user.save()
        return Response({'message': 'User deactivated'})


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
