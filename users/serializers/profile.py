from rest_framework import serializers

from users.models import Profile, DjangoUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ['username', 'email', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'avatar', 'title', 'bio', 'last_seen', 'rewards']


class CurrentUserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'display_name', 'avatar', 'title', 'bio', 'last_seen', 'rewards',
                  'vk_id', 'total_redirects', 'total_redirected', 'daily_redirects', 'daily_redirected']


class UserModeratorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
