from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.public_settings import DOMAIN
from users.serializers.login import LoginSerializer
from django_hyperlink.serializers.default import DefaultSerializer


class LoginView(APIView):

	serializer_class = LoginSerializer

	def post(self, request):
		serializer = self.serializer_class(data=request.data, request=request)
		if not serializer.is_valid():
			raise ParseError(DefaultSerializer.get_error_message(serializer))
		result = serializer.login()
		return Response(DefaultSerializer({
			'msg': "ok",
			'content': result
		}).data)