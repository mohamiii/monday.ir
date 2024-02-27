from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer
from rest_framework import status


class UserRegister(APIView):
    def post(self, request):
        validated_data = UserRegisterSerializer(data=request.POST)
        if validated_data.is_valid():
            validated_data.create(validated_data.validated_data)
            return Response(validated_data.data, status=status.HTTP_201_CREATED)
        return Response(validated_data.errors, status=status.HTTP_400_BAD_REQUEST)
