from django.urls import path

from .views import login, activate

urlpatterns = [
	path('login/', login, name='login'),
	path('activate/', activate, name='activate'),
	# path('register/', register, name='register')
]