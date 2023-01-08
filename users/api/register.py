from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from users.serializers.register import RegisterSerializer
from django_hyperlink.serializers.default import DefaultSerializer


class RegisterView(APIView):
	permission_classes = (permissions.AllowAny, )

	def post(self, request):

		serializer = RegisterSerializer(data=request.data)
		if not serializer.is_valid():
			raise ParseError(DefaultSerializer.get_error_message(serializer))
		serializer.create(serializer.validated_data)
		return Response(DefaultSerializer({
			'msg': 'Регистрация успешна! На ваш Email была отправлена ссылка для активации аккаунта',
			'content': serializer.data
		}).data)

