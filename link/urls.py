from django.urls import path, re_path

from .views import *

urlpatterns = [
	path('', index, name='index'),
	path('index/', index, name='named_index'),
]