from django.contrib import admin

from users.models import ActivateCode, User, DjangoUser

# Register your models here.


@admin.register(ActivateCode)
class ActivateCodeAdmin(admin.ModelAdmin):
	list_display = ('id', 'code', 'user', 'activated_date')
	list_display_links = ('id', 'code')
	readonly_fields = ('activated_date', 'is_used', 'expired_date', 'code')


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
	readonly_fields = ('user',)


class DjangoAdminUser(admin.ModelAdmin):
	verbose_name = 'Джанго пользователь'
	readonly_fields = ('username', 'email', 'date_joined')


admin.site.unregister(DjangoUser)
admin.site.register(DjangoUser, DjangoAdminUser)
