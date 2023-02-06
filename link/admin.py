from django.contrib import admin

from .models import ShareLink, LinkRedirect


# Register your models here.
@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
	pass


@admin.register(LinkRedirect)
class LinkRedirectAdmin(admin.ModelAdmin):
	pass