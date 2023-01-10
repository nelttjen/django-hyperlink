from django.urls import path

from .views import *

urlpatterns = [
	path('login/', login, name='users-login'),
	path('activate/', activate, name='users-activate'),
	path('register/', register, name='users-register'),
	path('test/', test, name='users-test')
]