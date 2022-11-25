from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = ()

    def post(self, request: Request):
        if request.data.get('password') != request.data.get('password2'):
            return Response({'message': 'password not equal', 'show_message': 'Пароли не совпадают.'}, status=400)

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            create = serializer.create(serializer.validated_data)
            if create == 'username':
                return Response({'message': 'username taken', 'show_message': ''})





class TestView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response({'status': 'ok'})