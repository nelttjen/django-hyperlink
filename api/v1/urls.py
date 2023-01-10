from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import *

link_patterns = [

]

users_patterns = [
	path('users/register/', RegisterView.as_view(), name='api-register'),
	path('users/activate/', ActivateView.as_view(), name='api-activate'),
	path('users/login/', obtain_auth_token, name='api-login'),
	path('users/test/', TestView.as_view(), name='api-test'),
]

urlpatterns = [
	*link_patterns,
	*users_patterns,
]