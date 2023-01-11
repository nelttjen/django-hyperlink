from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.public_settings import DOMAIN
from users.serializers.recovery import RecoverySerializer
from django_hyperlink.serializers.default import DefaultSerializer


class RecoveryView(APIView):
	permission_classes = (permissions.AllowAny, )

	def post(self, request):
		serializer = RecoverySerializer(data=request.data, method='post')
		if not serializer.is_valid():
			raise ParseError(DefaultSerializer.get_error_message(serializer))
		serializer.send_mail()
		return Response(DefaultSerializer({
			'msg': 'На ваш email, указанный при регистрации был отправлен код подтверждения'
		}).data)

	def put(self, request):
		serializer = RecoverySerializer(data=request.data, method='put')
		if not serializer.is_valid():
			raise ParseError(DefaultSerializer.get_error_message(serializer))
		serializer.recovery_user()
		return Response(DefaultSerializer({
			'msg': 'Пароль изменен. Теперь вы можете войти, используя новый пароль',
			'content': {
				"link": f"{DOMAIN}/users/login/"
			}
		}).data)