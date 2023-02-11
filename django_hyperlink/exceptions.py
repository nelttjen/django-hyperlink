from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from django_hyperlink.serializers.default import DefaultSerializer


def custom_exception_handler(exc, context):
	response = exception_handler(exc, context)

	if response:
		if not isinstance(exc, ValidationError):
			response.data = DefaultSerializer({'errors': {'msg': str(exc)}}).data
		else:
			errors = {'details': False}
			for key in exc.detail:
				if key == 'non_field_errors':
					errors['msg'] = exc.detail[key][0]
				else:
					errors['details'] = True
					detail = {'string': exc.detail[key][0], 'code': exc.detail[key][0].code}
					errors[key] = detail

			response.data = DefaultSerializer({'errors': errors}).data

	return response
