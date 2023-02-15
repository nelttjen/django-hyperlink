from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from rest_framework import permissions

from django_hyperlink.serializers.default import DefaultSerializer
from users.serializers.profile import UserProfileSerializer, CurrentUserProfileSerializer, \
    UserModeratorProfileSerializer, UpdateUserProfileSerializer
from users.models import Profile


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def _get_user(self, user_id, is_admin):
        try:
            user = Profile.objects.select_related('user').prefetch_related('rewards').get(user_id=user_id)
            ban, msg = user.check_ban()

            if ban and not is_admin:
                raise ParseError(_('Пользователь заблокирован на сайте'))

        except Profile.DoesNotExist:
            raise ParseError(_('Пользователь не найден'))
        return user

    def get(self, request, user_id):

        is_admin = request.user.is_authenticated and request.user.is_staff

        user = self._get_user(user_id, is_admin)

        if is_admin and request.user.id != user.user_id:
            serializer = UserModeratorProfileSerializer
        elif request.user.id == user.user_id:
            serializer = CurrentUserProfileSerializer
        else:
            serializer = UserProfileSerializer

        return Response(DefaultSerializer({'content': serializer(user).data}).data)

    def put(self, request, user_id):
        profile = self._get_user(user_id, request.user.is_staff)

        serializer = UpdateUserProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        profile = self._get_user(user_id, request.user.is_staff)

        return Response(DefaultSerializer({'content': CurrentUserProfileSerializer(profile).data}).data)


