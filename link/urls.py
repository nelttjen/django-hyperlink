from django.urls import path, re_path

from .views import index, login

urlpatterns = [
	path('', index, name='index'),
	path('index/', index, name='named_index'),
	path('login/', login, name='login',)
]