import datetime

from django.db.models import F, Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from link.tasks.links import update_link_redirects
from link.models import ShareLink
from users.modules import get_ip


class ShareLinkSerializer(serializers.ModelSerializer):
    valid_until_as_timestamp = serializers.IntegerField(required=False)
    date_created_as_timestamp = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        is_owner = False
        add_timestamp = False
        if 'is_owner' in kwargs.keys():
            is_owner = kwargs.pop('is_owner')
        if 'add_timestamp' in kwargs.keys():
            add_timestamp = kwargs.pop('add_timestamp')

        super().__init__(*args, **kwargs)

        self.Meta.fields = ['redirect_timer', 'redirect_to']
        if is_owner:
            self.Meta.fields.extend(
                ['share_code', 'valid_until', 'is_active', 'redirects',
                 'allowed_redirects', 'date_created', 'only_unique_redirects']
            )
        if add_timestamp:
            self.Meta.fields.extend(['valid_until_as_timestamp', 'date_created_as_timestamp'])

    class Meta:
        model = ShareLink

    @staticmethod
    def get_link(request, code):
        if not request.user.is_authenticated:
            setattr(request.user, 'id', -1)

        link = ShareLink.objects.filter(share_code=code).filter(
            ((Q(redirects__lt=F('allowed_redirects')) | Q(allowed_redirects=-1)) & Q(is_active=True) &
             (Q(valid_until__gt=timezone.now()) | Q(valid_until__isnull=True))) | Q(owner_id=request.user.id)
        ).first()

        return link

    @staticmethod
    def redirect(request, code):
        ip = get_ip(request)
        user_id = request.user.id if request.user.is_authenticated else None

        if not (link := ShareLink.objects.filter(share_code=code).only('id', 'only_unique_redirects').first()):
            return False

        update_link_redirects.delay(link.id, user_id, ip, is_unique=link.only_unique_redirects)
        return True


class ShareLinkCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShareLink
        fields = '__all__'


class ShareLinkUpdateSerializer(serializers.ModelSerializer):

    def update(self, instance, data):
        if valid_until := data.get('valid_until'):
            if valid_until not in (1, 7, 30, -1):
                raise serializers.ValidationError(_('Время должно быть 1, 7, 30 дней или бессрочно'))
            if instance.valid_until < timezone.now():
                raise serializers.ValidationError(_('Ссылка уже истекла'))
            instance.valid_until = (timezone.now() + datetime.timedelta(days=valid_until)) if valid_until else None

        super().update(instance, data)

    class Meta:
        model = ShareLink
        fields = ('redirect_timer', 'valid_until', 'allowed_redirects', 'only_unique_redirects', 'is_active')