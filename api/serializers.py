from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class RegisterSerializer(ModelSerializer):

	class Meta:
		model = User
		fields = (
			'username',
			'email',
			'password',
		)

		extra_kwargs = {'password': {'write_only': True}}

	def create(self, validated_data):
		if User.objects.filter(username=validated_data['username']).first():
			return 'username'
		if User.objects.filter(email=validated_data['email']).first():
			return 'email'
		user = User.objects.create_user(
			username=validated_data['username'],
			password=validated_data['password'],
			email=validated_data['email'],
		)
		return user
