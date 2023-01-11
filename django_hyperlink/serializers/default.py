from rest_framework import serializers

from django_hyperlink.settings import DEBUG


class DefaultSerializer(serializers.Serializer):
	msg = serializers.CharField(default='')
	content = serializers.JSONField(default=[])
	extra = serializers.JSONField(default={})

	@staticmethod
	def get_error_message(serializer):
		errors = []
		if DEBUG:
			print(serializer.errors)
		for options in serializer.errors.values():
			try:
				for message in options:
					errors.append(message.__str__())
			except:
				errors.append(options.__str__())
		return ', '.join(errors)