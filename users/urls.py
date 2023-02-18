from django.urls import path

from .views import *

urlpatterns = [
	path('login/', login, name='users-login'),
	path('logout/', logout, name='users-logout'),
	path('activate/', activate, name='users-activate'),
	path('register/', register, name='users-register'),
	path('test/', test, name='users-test'),
	path('recovery/', recovery, name='users-recovery'),
	path('profile/', profile, name='users-profile'),

	path('login/socials/', socials, name='socials'),
	path('login/socials/vk/process/', socials_vk, name='socials-process-vk'),
]