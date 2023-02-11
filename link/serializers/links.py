from django.db.models import F, Q
from django.utils import timezone
from rest_framework import serializers

from link.tasks.links import update_link_redirects
from link.models import ShareLink
from users.modules import get_ip


class ShareLinkSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        is_owner = False
        if 'is_owner' in kwargs.keys():
            is_owner = kwargs.pop('is_owner')
        super().__init__(*args, **kwargs)

        self.Meta.fields = ['redirect_timer', 'redirect_to']
        if is_owner:
            self.Meta.fields.extend(
                ['share_code', 'valid_until', 'is_active', 'redirects',
                 'allowed_redirects', 'date_created', 'only_unique_redirects']
            )

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
