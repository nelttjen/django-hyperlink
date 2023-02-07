from django.urls import path, re_path

from .views import *

urlpatterns = [
	path('new/', create, name='create'),

	path('<str:code>/', index, name='index'),
]