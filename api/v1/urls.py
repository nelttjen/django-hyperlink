from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import *

link_patterns = [

]

users_patterns = [
	path('users/register/', RegisterView.as_view()),
	path('users/activate/', ActivateView.as_view()),
	path('users/login/', obtain_auth_token),
]

urlpatterns = [
	*link_patterns,
	*users_patterns,
]