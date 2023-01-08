from rest_framework.views import exception_handler
from django_hyperlink.serializers.default import DefaultSerializer


def custom_exception_handler(exc, context):
	response = exception_handler(exc, context)

	if response:
		response.data = DefaultSerializer({'msg': exc}).data

	return response
