from django.contrib import admin

from .models import ShareLink


# Register your models here.
class ShareLinkAdmin(admin.ModelAdmin):
    pass


admin.site.register(ShareLink, ShareLinkAdmin)
