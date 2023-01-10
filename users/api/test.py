from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.serializers.default import DefaultSerializer


class TestView(APIView):
	permission_classes = (permissions.IsAuthenticated, )

	def post(self, request):
		print(request.headers)
		print(request.user.id, request.user)
		return Response(DefaultSerializer({
			'msg': 'ok'
		}).data)
