from rest_framework import serializers


class DefaultSerializer(serializers.Serializer):
	msg = serializers.CharField(default='')
	content = serializers.JSONField(default=[])
	extra = serializers.JSONField(default={})

	@staticmethod
	def get_error_message(serializer):
		errors = []
		for options in serializer.errors.values():
			try:
				for message in options:
					errors.append(message.__str__())
			except:
				errors.append(options.__str__())
		return ', '.join(errors)