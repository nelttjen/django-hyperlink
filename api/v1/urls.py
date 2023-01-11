from django.urls import path

from . import *

link_patterns = [

]

users_patterns = [
	path('users/register/', RegisterView.as_view(), name='api-register'),
	path('users/activate/', ActivateView.as_view(), name='api-activate'),
	path('users/login/', LoginView.as_view(), name='api-login'),
	path('users/test/', TestView.as_view(), name='api-test'),
	path('users/recovery/', RecoveryView.as_view(), name='api-recovery'),
]

urlpatterns = [
	*link_patterns,
	*users_patterns,
]